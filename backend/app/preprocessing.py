"""Notebook-matched image decoding, 160×160 resize, and ResNet50 preprocessing."""
from __future__ import annotations

import tensorflow as tf

IMAGE_SIZE = (160, 160)


def prepare_image(image_bytes: bytes) -> tf.Tensor:
    """Mirror the selected notebook's decode, resize, and ResNet50 pipeline."""
    decoded = tf.io.decode_image(
        image_bytes,
        channels=3,
        expand_animations=False,
        dtype=tf.uint8,
    )
    decoded.set_shape((None, None, 3))
    resized = tf.image.resize(
        tf.cast(decoded, tf.float32),
        IMAGE_SIZE,
        method="bilinear",
        antialias=False,
    )
    normalized = tf.keras.applications.resnet50.preprocess_input(resized)
    return tf.expand_dims(normalized, axis=0)
