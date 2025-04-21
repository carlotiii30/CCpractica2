import unittest
from handler import handle


class TestFaceDetectionFunction(unittest.TestCase):
    def test_valid_url(self):
        image_url = "https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg"
        response = handle(image_url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("image/jpeg", response.headers["Content-Type"])
        self.assertIsInstance(response.data, bytes)
        self.assertGreater(len(response.data), 1000)


if __name__ == "__main__":
    unittest.main()
