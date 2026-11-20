from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

Fruit = Literal["Apel", "Pisang", "Jeruk"]
Status = Literal["fresh", "rotten"]

FRUIT_BY_CLASS: dict[int, Fruit] = {
    0: "Apel",
    1: "Pisang",
    2: "Jeruk",
    3: "Apel",
    4: "Pisang",
    5: "Jeruk",
}
ROTTEN_CLASS_IDS = frozenset({3, 4, 5})


@dataclass(frozen=True)
class Decision:
    status: Status
    fruit: Fruit | None
    reason: str


def decide(scores: np.ndarray) -> Decision:
    """Map the six-class ResNet50 argmax to its fruit and freshness label."""
    values = np.asarray(scores, dtype=np.float32).reshape(-1)
    if values.size != 6 or not np.isfinite(values).all():
        raise ValueError("Output ResNet50 harus berisi enam skor finite.")

    top_class = int(np.argmax(values))
    fruit = FRUIT_BY_CLASS[top_class]
    if top_class in ROTTEN_CLASS_IDS:
        return Decision(
            status="rotten",
            fruit=fruit,
            reason="Perkiraan visual dari model ResNet50.",
        )

    return Decision(
        status="fresh",
        fruit=fruit,
        reason="Perkiraan visual dari model ResNet50.",
    )
