"""Utilities for scanning and classifying media files on disk."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Tuple

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


def scan_media(directory: Path) -> Tuple[List[Dict[str, str]], int]:
    """Return media files found under *directory* recursively.

    Returns a tuple ``(files, skipped)`` where ``files`` is a list of
    discovered media dictionaries and ``skipped`` is the number of entries
    that could not be accessed due to permission errors.
    """

    files: List[Dict[str, str]] = []
    skipped = 0

    for root, _, filenames in os.walk(directory, onerror=lambda e: None):
        for name in filenames:
            path = Path(root) / name
            try:
                ext = path.suffix.lower()
                if ext in MEDIA_EXTENSIONS:
                    info: Dict[str, str] = {"path": str(path)}
                    if ext in IMAGE_EXTENSIONS:
                        info["label"] = classify_image(path)
                    files.append(info)
            except (OSError, PermissionError):
                skipped += 1

    return files, skipped
