"""Flask-based web interface for browsing media files."""
from __future__ import annotations

from pathlib import Path
import io
from flask import Flask, jsonify, request, send_from_directory, send_file, abort
from PIL import Image

try:
    import pillow_heif
    pillow_heif.register_heif_opener()  # enable HEIC support if installed
except Exception:  # pragma: no cover - pillow-heif is optional
    pass

from .face import detect_faces
from .database import init_db, add_face_tag, search_by_name
from .tasks import scan_media_task

STATIC_DIR = Path(__file__).resolve().parents[1] / "frontend"
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")
init_db()



@app.post("/api/scan")
def api_scan() -> object:
    """Kick off a background scan task for *path*."""
    data = request.get_json(force=True)
    path_str = data.get("path", ".")
    task = scan_media_task.delay(path_str)
    return jsonify({"task_id": task.id})


@app.get("/api/scan/<task_id>")
def api_scan_status(task_id: str) -> object:
    """Return status information for a scan task."""
    task = scan_media_task.AsyncResult(task_id)
    if task.state == "PENDING":
        return jsonify({"state": "PENDING", "progress": 0})
    if task.state == "FAILURE":
        return jsonify({"state": "FAILURE", "error": str(task.info)}), 500
    meta = task.info or {}
    current = meta.get("current", 0)
    total = meta.get("total", 1)
    meta.update({"state": task.state, "progress": current / total if total else 0})
    return jsonify(meta)


@app.get("/api/dirs")
def api_dirs() -> object:
    """Return subdirectories for *path* as JSON."""
    path_str = request.args.get("path", ".")
    directory = Path(path_str)
    dirs = [str(p) for p in directory.iterdir() if p.is_dir()]
    return jsonify(dirs)


@app.get("/api/file")
def api_file() -> object:
    """Send a media file to the browser.

    HEIC images are converted to JPEG on the fly for browser compatibility.
    """
    path_str = request.args.get("path")
    if not path_str:
        abort(400)
    path = Path(path_str)
    if not path.exists():
        abort(404)
    if path.suffix.lower() == ".heic":
        with Image.open(path) as img:
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            buf.seek(0)
            return send_file(buf, mimetype="image/jpeg")
    return send_file(path)


@app.post("/api/tag")
def api_tag() -> object:
    data = request.get_json(force=True)
    path = Path(data.get("path", ""))
    name = data.get("name")
    if not path or not name:
        abort(400)
    faces = detect_faces(path)
    if not faces:
        return jsonify({"status": "no-face"}), 400
    add_face_tag(str(path), name, faces[0])
    return jsonify({"status": "ok"})


@app.get("/api/search")
def api_search() -> object:
    name = request.args.get("name")
    if not name:
        abort(400)
    paths = search_by_name(name)
    # return basic file records; labels will be looked up via DB by client if needed
    files = [{"path": p} for p in paths]
    return jsonify(files)


@app.route("/")
def index() -> object:
    """Serve the React application."""
    return send_from_directory(app.static_folder, "index.html")


def run_server() -> None:
    """Run the development server."""
    app.run(host="0.0.0.0", port=5000, debug=True)
