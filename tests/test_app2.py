from flask import Flask, request, jsonify
from flask.testing import FlaskClient
from app import app
import unittest

restaurants = [
    {
        "city": "Helsinki",
        "currency": "EUR",
        "delivery_price": 390,
        "description": "Japanilaista ramenia parhaimmillaan",
        "image": "https://prod-wolt-venue-images-cdn.wolt.com/5d108aa82e757db3f4946ca9/d88ebd36611a5e56bfc6a60264fe3f81",
        "location": [24.941786527633663, 60.169934599421396],
        "name": "Momotoko Citycenter",
        "online": False,
        "tags": ["ramen", "risotto"],
        "blurhash": "j2DUFG8jbu8AXuLIT5Tt0B01R2;;"
    },
    {
        "city": "Helsinki",
        "currency": "EUR",
        "delivery_price": 390,
        "description": "Kiinalaista buffetia parhaimmillaan",
        "image": "https://prod-wolt-venue-images-cdn.wolt.com/5d108aa82e757db3f4946ca9/d88ebd36611a5e56bfc6a60264fe3f81",
        "location": [24.9677737, 60.2029952],
        "name": "Kuwano",
        "online": False,
        "tags": ["chinese", "buffeti"],
        "blurhash": "j2DUFG8jbu8AXuLIT5Tt0B01R2;;"
    }
]


class TestRestaurants(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.client = app.test_client()

    def tearDown(self):
        pass  # Clean up resources if needed

    def test_get_restaurant(self):
        response = self.client.get('/restaurants')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, restaurants)


if __name__ == "__main__":
    unittest.main()
