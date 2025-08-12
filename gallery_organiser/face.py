"""Simple face detection utilities using OpenCV."""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

try:  # pragma: no cover - optional dependency
    import cv2
except Exception:  # pragma: no cover
    cv2 = None  # type: ignore

_cascade = None


def _load_cascade() -> None:
    global _cascade
    if cv2 is None:  # pragma: no cover
        return
    if _cascade is None:
        _cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def detect_faces(path: Path) -> List[Tuple[int, int, int, int]]:
    """Return a list of face bounding boxes for the image at *path*."""
    if cv2 is None:  # pragma: no cover
        return []
    _load_cascade()
    if _cascade is None:
        return []
    img = cv2.imread(str(path))
    if img is None:
        return []
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = _cascade.detectMultiScale(gray, 1.1, 4)
    return [tuple(map(int, f)) for f in faces]
