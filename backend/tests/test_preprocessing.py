import io
import unittest

import numpy as np
from PIL import Image

from backend.app.preprocessing import prepare_image


class PreprocessingTests(unittest.TestCase):
    def test_supported_formats_produce_finite_160_square_rgb_tensor(self) -> None:
        for image_format in ("PNG", "JPEG", "WEBP"):
            with self.subTest(image_format=image_format):
                encoded = io.BytesIO()
                Image.new("RGB", (37, 29), (120, 40, 210)).save(encoded, format=image_format)
                tensor = prepare_image(encoded.getvalue()).numpy()
                self.assertEqual(tensor.shape, (1, 160, 160, 3))
                self.assertEqual(tensor.dtype, np.float32)
                self.assertTrue(np.isfinite(tensor).all())

    def test_rgb_input_uses_resnet50_caffe_channel_order_and_means(self) -> None:
        encoded = io.BytesIO()
        Image.new("RGB", (16, 16), (255, 0, 0)).save(encoded, format="PNG")
        tensor = prepare_image(encoded.getvalue()).numpy()
        np.testing.assert_allclose(
            tensor[0, 80, 80],
            [-103.939, -116.779, 131.32],
            rtol=0,
            atol=0.002,
        )


if __name__ == "__main__":
    unittest.main()
