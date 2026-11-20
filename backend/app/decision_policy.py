from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

Fruit = Literal["Apel", "Pisang", "Jeruk"]
Status = Literal["rotten", "review"]

FRUIT_BY_CLASS = {
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
    """Turn six-class output into a safety-first result.

    Fresh is deliberately not an output yet: the complete validation split is
    unavailable locally and the notebook's raw argmax report contains false-
    fresh predictions. A rotten top class may be reported as rotten; every
    other valid result is sent to review until a separate safety policy passes.
    """
    values = np.asarray(scores, dtype=np.float32).reshape(-1)
    if values.size != 6 or not np.isfinite(values).all():
        return Decision(
            status="review",
            fruit=None,
            reason="Hasil model belum dapat dibaca. Periksa buah secara langsung.",
        )

    top_class = int(np.argmax(values))
    fruit = FRUIT_BY_CLASS[top_class]
    if top_class in ROTTEN_CLASS_IDS:
        return Decision(
            status="rotten",
            fruit=fruit,  # type: ignore[arg-type]
            reason="Ciri visual model mengarah ke buah busuk. Periksa kembali seluruh permukaan buah.",
        )

    return Decision(
        status="review",
        fruit=fruit,  # type: ignore[arg-type]
        reason="Label Segar otomatis belum aktif karena kalibrasi keselamatan pada data lengkap belum lulus.",
    )
