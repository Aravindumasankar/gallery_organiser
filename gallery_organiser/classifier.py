"""Image classification utilities using a pre-trained ResNet model.

The classifier lazily loads the model on first use to avoid import costs
when image classification is not required. If any part of the loading or
classification fails, the function returns ``"unknown"`` so callers can
handle environments without the necessary ML dependencies.
"""
from __future__ import annotations

from pathlib import Path
from typing import List

from PIL import Image

try:  # pragma: no cover - heavy dependency optional
    import torch
    from torchvision.models import resnet18, ResNet18_Weights
except Exception:  # pragma: no cover - fall back when torch is missing
    torch = None  # type: ignore

_model = None
_transform = None
_labels: List[str] = []


def _load_model() -> None:
    """Load the pre-trained model and preprocessing transforms."""
    global _model, _transform, _labels
    if torch is None:  # pragma: no cover - torch not available
        return
    weights = ResNet18_Weights.DEFAULT
    _model = resnet18(weights=weights)
    _model.eval()
    _transform = weights.transforms()
    _labels = weights.meta.get("categories", [])


def classify_image(path: Path) -> str:
    """Return the best-guess label for the image at *path*.

    If the model or dependencies are unavailable, ``"unknown"`` is
    returned instead of raising an exception.
    """
    try:
        if _model is None:
            _load_model()
        if _model is None or torch is None:
            return "unknown"
        img = Image.open(path).convert("RGB")
        tensor = _transform(img).unsqueeze(0)
        with torch.no_grad():
            preds = _model(tensor)[0]
        idx = int(preds.argmax())
        if 0 <= idx < len(_labels):
            return _labels[idx]
    except Exception:  # pragma: no cover - best effort only
        pass
    return "unknown"
