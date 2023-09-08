from flask import Flask, request, jsonify
from flask.testing import FlaskClient
# from app import app
import unittest


class TestHelloWorld(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = Flask(__name__)
        self.client = self.app.test_client()

        #Define the route '/' with a view function
        @self.app.route('/')
        def helloworld():
            data = {"data": "Hello World"}
            return jsonify(data)

    def tearDown(self):
        pass  # Clean up resources if needed

    def test_helloworld(self):
        with self.app.test_request_context('/'):
            response = self.client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {"data": "Hello World"})


if __name__ == "__main__":
    unittest.main()