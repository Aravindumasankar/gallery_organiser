"""Image classification utilities using a Hugging Face model.

The classifier lazily loads the model on first use to avoid heavy imports
when classification is not required. If loading fails, ``"unknown"`` is
returned so callers can handle environments without the ML dependencies.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

try:  # pragma: no cover - heavy dependency optional
    from transformers import pipeline
except Exception:  # pragma: no cover - transformers not available
    pipeline = None  # type: ignore

_classifier = None


def _load_model() -> None:
    """Load the image classification pipeline."""
    global _classifier
    if pipeline is None:  # pragma: no cover - transformers missing
        return
    _classifier = pipeline("image-classification")


def classify_image(path: Path) -> str:
    """Return the best-guess label for the image at *path*.

    Falls back to ``"unknown"`` if the model or dependencies are
    unavailable.
    """
    try:
        if _classifier is None:
            _load_model()
        if _classifier is None:
            return "unknown"
        preds = _classifier(str(path))
        if preds:
            return preds[0]["label"]
    except Exception:  # pragma: no cover - best effort only
        pass
    return "unknown"
