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

from .media import scan_media

STATIC_DIR = Path(__file__).resolve().parents[1] / "frontend"
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")


@app.get("/api/media")
def api_media() -> object:
    """Return media files under a given directory as JSON.

    Each item includes the file ``path`` and, for images, a ``label`` from
    the classifier.
    """
    path_str = request.args.get("path", ".")
    files, skipped = scan_media(Path(path_str))
    return jsonify({"files": files, "skipped": skipped})


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


@app.route("/")
def index() -> object:
    """Serve the React application."""
    return send_from_directory(app.static_folder, "index.html")


def run_server() -> None:
    """Run the development server."""
    app.run(host="0.0.0.0", port=5000, debug=True)
