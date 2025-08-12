"""Flask-based web interface for browsing media files."""
from __future__ import annotations

from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory

from .media import scan_media

STATIC_DIR = Path(__file__).resolve().parents[1] / "frontend"
app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")


@app.get("/api/media")
def api_media() -> object:
    """Return media files under a given directory as JSON."""
    path_str = request.args.get("path", ".")
    files = [str(p) for p in scan_media(Path(path_str))]
    return jsonify(files)


@app.route("/")
def index() -> object:
    """Serve the React application."""
    return send_from_directory(app.static_folder, "index.html")


def run_server() -> None:
    """Run the development server."""
    app.run(debug=True)
