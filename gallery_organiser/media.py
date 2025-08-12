"""Utilities for scanning media files on disk."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable, List

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


def scan_media(directory: Path) -> List[Path]:
    """Return media files found under *directory* recursively."""
    files: List[Path] = []
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in MEDIA_EXTENSIONS:
            files.append(path)
    return files
