import unittest
from handler import handle

class TestFaceDetectionFunction(unittest.TestCase):
    def test_valid_url(self):
        image_url = "https://upload.wikimedia.org/wikipedia/commons/3/37/Dagestani_man_and_woman.jpg"
        response = handle(image_url)

        self.assertEqual(response["statusCode"], 200)
        self.assertIn("image/jpeg", response["headers"]["Content-Type"])
        self.assertIsInstance(response["body"], bytes)
        self.assertGreater(len(response["body"]), 1000)

    def test_invalid_url(self):
        image_url = "https://example.com/invalid.jpg"
        response = handle(image_url)

        self.assertEqual(response["statusCode"], 500)
        self.assertIn("Error procesando la imagen", response["body"])

if __name__ == '__main__':
    unittest.main()
