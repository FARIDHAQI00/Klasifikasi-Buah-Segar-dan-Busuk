"""Map six model class scores to the fruit name and Segar/Busuk result."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import numpy as np

Fruit = Literal["Apel", "Pisang", "Jeruk"]
Status = Literal["fresh", "rotten"]
ReportedFruit = Fruit | Literal["Campuran"]

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
    fruit: ReportedFruit | None
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


def decide_regions(region_scores: Iterable[np.ndarray]) -> Decision:
    """Aggregate fruit-region predictions, treating any rotten region as rotten."""
    decisions = [decide(scores) for scores in region_scores]
    if not decisions:
        raise ValueError("Tidak ada bagian buah untuk dinilai.")

    fruits = {decision.fruit for decision in decisions if decision.fruit is not None}
    fruit: ReportedFruit | None = next(iter(fruits)) if len(fruits) == 1 else "Campuran"
    has_rotten_region = any(decision.status == "rotten" for decision in decisions)
    if has_rotten_region:
        return Decision(
            status="rotten",
            fruit=fruit,
            reason="Ada bagian buah yang diperkirakan busuk.",
        )

    return Decision(
        status="fresh",
        fruit=fruit,
        reason="Semua bagian buah yang terdeteksi diperkirakan segar.",
    )
