"""Utilities for scanning and classifying media files on disk."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List

from .classifier import classify_image

MEDIA_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".heic",
    ".mp4",
    ".mov",
    ".mkv",
}

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".heic",
}


def scan_media(directory: Path) -> List[Dict[str, str]]:
    """Return media files found under *directory* recursively.

    Each item in the returned list contains a ``path`` key. Images include
    an additional ``label`` key populated by the classifier.
    """

    files: List[Dict[str, str]] = []
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in MEDIA_EXTENSIONS:
            info: Dict[str, str] = {"path": str(path)}
            if path.suffix.lower() in IMAGE_EXTENSIONS:
                info["label"] = classify_image(path)
            files.append(info)
    return files
