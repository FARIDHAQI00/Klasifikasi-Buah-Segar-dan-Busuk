"""Checks six-class argmax mapping, fruit labels, ties, and invalid model scores."""
import unittest

import numpy as np

from backend.app.decision_policy import decide, decide_regions


class DecisionPolicyTests(unittest.TestCase):
    def test_fresh_argmax_returns_fresh(self) -> None:
        for class_id in range(3):
            with self.subTest(class_id=class_id):
                scores = np.zeros(6, dtype=np.float32)
                scores[class_id] = 1.0
                result = decide(scores)
                self.assertEqual(result.status, "fresh")
                self.assertIsNotNone(result.fruit)

    def test_rotten_argmax_returns_rotten(self) -> None:
        for class_id in range(3, 6):
            with self.subTest(class_id=class_id):
                scores = np.zeros(6, dtype=np.float32)
                scores[class_id] = 1.0
                result = decide(scores)
                self.assertEqual(result.status, "rotten")
                self.assertIsNotNone(result.fruit)

    def test_argmax_tie_uses_first_class(self) -> None:
        result = decide([0.5, 0.0, 0.0, 0.5, 0.0, 0.0])
        self.assertEqual(result.status, "fresh")

    def test_invalid_scores_raise_error(self) -> None:
        invalid_scores = (
            [],
            [0.0] * 5,
            [0.0] * 7,
            [0.0, 0.0, 0.0, float("nan"), 0.0, 0.0],
            [0.0, 0.0, 0.0, float("inf"), 0.0, 0.0],
        )
        for scores in invalid_scores:
            with self.subTest(scores=scores):
                with self.assertRaises(ValueError):
                    decide(scores)

    def test_any_rotten_region_makes_the_photo_rotten(self) -> None:
        fresh_banana = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
        rotten_banana = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0]

        result = decide_regions([fresh_banana, rotten_banana])

        self.assertEqual(result.status, "rotten")
        self.assertEqual(result.fruit, "Pisang")

    def test_fresh_regions_remain_fresh(self) -> None:
        result = decide_regions(
            [
                [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            ]
        )

        self.assertEqual(result.status, "fresh")
        self.assertEqual(result.fruit, "Campuran")

    def test_empty_region_list_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            decide_regions([])


if __name__ == "__main__":
    unittest.main()
