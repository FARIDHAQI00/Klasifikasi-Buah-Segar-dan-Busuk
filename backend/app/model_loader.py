from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from threading import Lock
from typing import Any

os.environ.setdefault("TF_NUM_INTRAOP_THREADS", "1")
os.environ.setdefault("TF_NUM_INTEROP_THREADS", "1")

import tensorflow as tf

MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
MODEL_PATH = MODEL_DIR / "ResNet50_terbaik.keras"
MANIFEST_PATH = MODEL_DIR / "model_manifest.json"
_MODEL: tf.keras.Model | None = None
_MANIFEST: dict[str, Any] | None = None
_LOAD_LOCK = Lock()


def read_manifest() -> dict[str, Any]:
    global _MANIFEST
    if _MANIFEST is None:
        _MANIFEST = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return _MANIFEST


def model_path() -> Path:
    return MODEL_PATH


def load_model() -> tf.keras.Model:
    global _MODEL
    if _MODEL is not None:
        return _MODEL

    with _LOAD_LOCK:
        if _MODEL is None:
            if not MODEL_PATH.is_file():
                raise RuntimeError("Artefak ResNet50 tidak ditemukan di backend/model.")

            manifest = read_manifest()
            expected_hash = manifest.get("sha256")
            digest = hashlib.sha256()
            with MODEL_PATH.open("rb") as model_file:
                for chunk in iter(lambda: model_file.read(1024 * 1024), b""):
                    digest.update(chunk)
            actual_hash = digest.hexdigest()
            if not expected_hash or actual_hash.lower() != expected_hash.lower():
                raise RuntimeError("Hash artefak ResNet50 tidak sesuai manifest.")

            _MODEL = tf.keras.models.load_model(MODEL_PATH, compile=False)

    return _MODEL


def predict(image_tensor: tf.Tensor) -> list[float]:
    model = load_model()
    output = model(image_tensor, training=False)
    values = output.numpy().reshape(-1).astype("float32")
    if values.size != 6:
        raise RuntimeError(f"Output ResNet50 berisi {values.size} kelas, seharusnya 6.")
    return [float(value) for value in values]
