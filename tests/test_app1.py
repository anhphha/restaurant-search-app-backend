from flask import Flask, request, jsonify
from flask.testing import FlaskClient
from app import app
import unittest

class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.client = app.test_client()

    def tearDown(self):
        pass  # Clean up resources if needed

    def test_helloworld(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"data": "Hello World"})


if __name__ == "__main__":
    unittest.main()