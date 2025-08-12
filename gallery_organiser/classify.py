"""Image classification utilities using a pre-trained ONNX model."""
from __future__ import annotations

from pathlib import Path
import json
import urllib.request
from typing import Tuple

import numpy as np
from PIL import Image
import onnxruntime as ort

MODEL_URL = "https://github.com/onnx/models/raw/main/vision/classification/squeezenet/model/squeezenet1.1-7.onnx"
LABELS_URL = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
CACHE_DIR = Path.home() / ".cache" / "gallery_organiser"
MODEL_PATH = CACHE_DIR / "squeezenet.onnx"
LABELS_PATH = CACHE_DIR / "labels.json"

_session: ort.InferenceSession | None = None
_labels: list[str] | None = None

def _download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        with urllib.request.urlopen(url) as resp, open(dest, "wb") as fh:
            fh.write(resp.read())

def _load() -> Tuple[ort.InferenceSession, list[str]]:
    global _session, _labels
    if _session is None or _labels is None:
        _download(MODEL_URL, MODEL_PATH)
        _download(LABELS_URL, LABELS_PATH)
        _session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])
        with open(LABELS_PATH) as fh:
            _labels = json.load(fh)
    return _session, _labels

def classify_image(path: str | Path) -> str:
    """Return an ImageNet class label for *path*.

    The first call downloads the model and label files into a cache directory.
    """
    session, labels = _load()
    img = Image.open(path).convert("RGB").resize((224, 224))
    arr = np.array(img).astype("float32") / 255.0
    arr = arr.transpose(2, 0, 1)  # CHW
    mean = np.array([0.485, 0.456, 0.406]).reshape(3, 1, 1)
    std = np.array([0.229, 0.224, 0.225]).reshape(3, 1, 1)
    arr = (arr - mean) / std
    arr = arr[None, :, :, :]  # add batch dim
    logits = session.run(None, {session.get_inputs()[0].name: arr})[0]
    idx = int(np.argmax(logits))
    return labels[idx]
