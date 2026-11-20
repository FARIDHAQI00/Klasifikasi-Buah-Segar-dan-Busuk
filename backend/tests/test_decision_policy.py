import unittest

import numpy as np

from backend.app.decision_policy import decide


class DecisionPolicyTests(unittest.TestCase):
    def test_fresh_argmax_never_returns_fresh(self) -> None:
        for class_id in range(3):
            with self.subTest(class_id=class_id):
                scores = np.zeros(6, dtype=np.float32)
                scores[class_id] = 1.0
                result = decide(scores)
                self.assertEqual(result.status, "review")
                self.assertIsNotNone(result.fruit)

    def test_rotten_argmax_returns_rotten(self) -> None:
        for class_id in range(3, 6):
            with self.subTest(class_id=class_id):
                scores = np.zeros(6, dtype=np.float32)
                scores[class_id] = 1.0
                result = decide(scores)
                self.assertEqual(result.status, "rotten")
                self.assertIsNotNone(result.fruit)

    def test_fresh_rotten_tie_falls_back_to_review(self) -> None:
        result = decide([0.5, 0.0, 0.0, 0.5, 0.0, 0.0])
        self.assertEqual(result.status, "review")

    def test_invalid_scores_fall_back_to_review(self) -> None:
        invalid_scores = (
            [],
            [0.0] * 5,
            [0.0] * 7,
            [0.0, 0.0, 0.0, float("nan"), 0.0, 0.0],
            [0.0, 0.0, 0.0, float("inf"), 0.0, 0.0],
        )
        for scores in invalid_scores:
            with self.subTest(scores=scores):
                result = decide(scores)
                self.assertEqual(result.status, "review")
                self.assertIsNone(result.fruit)


if __name__ == "__main__":
    unittest.main()
