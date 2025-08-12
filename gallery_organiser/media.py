"""Utilities for scanning and classifying media files on disk."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Callable, Dict, List, Tuple

from .classifier import classify_image
from .database import store_label

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


def scan_media(
    directory: Path,
    progress_cb: Callable[[int, int, List[str]], None] | None = None,
) -> Tuple[List[Dict[str, str]], int, List[str], int]:
    """Return media files found under *directory* recursively.

    Returns a tuple ``(files, skipped, logs, total)`` where ``files`` is a list
    of discovered media dictionaries, ``skipped`` is the number of entries that
    could not be accessed, ``logs`` contains textual activity messages, and
    ``total`` is the number of filesystem entries visited. When ``progress_cb``
    is supplied it will be called with ``(current, total, recent_logs)`` for
    every processed file allowing callers to track progress.
    """

    files: List[Dict[str, str]] = []
    skipped = 0
    logs: List[str] = []

    total = 0
    for _root, _dirs, filenames in os.walk(directory, onerror=lambda e: None):
        total += len(filenames)

    current = 0
    for root, _, filenames in os.walk(directory, onerror=lambda e: None):
        for name in filenames:
            path = Path(root) / name
            current += 1
            try:
                ext = path.suffix.lower()
                if ext in MEDIA_EXTENSIONS:
                    info: Dict[str, str] = {"path": str(path)}
                    logs.append(f"Found {path}")
                    if ext in IMAGE_EXTENSIONS:
                        label = classify_image(path)
                        info["label"] = label
                        store_label(str(path), label)
                        logs.append(f"Classified {path} as {label}")
                    files.append(info)
            except (OSError, PermissionError):
                skipped += 1
                logs.append(f"Skipped {path}")

            if progress_cb:
                progress_cb(current, total, logs[-10:])

    return files, skipped, logs, total
