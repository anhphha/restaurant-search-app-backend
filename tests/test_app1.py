from flask.testing import FlaskClient
from flask import Flask, request, jsonify

# Create a test client
app = Flask(__name__)
client = app.test_client()


@app.route('/')
def helloworld():
    if (request.method == 'GET'): # Use request.method to access the HTTP method
        data = {"data": "Hello World"}
        return jsonify(data)

def test_helloworld():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"data": "Hello World"}

if __name__ == "__main__":
    import pytest
    pytest.main()




# import unittest
# from flask import Flask
# from flask.testing import FlaskClient

# # Create a test client
# app = Flask(__name__)
# app.config['TESTING'] = True
# client = app.test_client()

# class APITestCase(unittest.TestCase):
#     def test_helloworld(self):
#         response = client.get('/')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json, {"data": "Hello World"})


# if __name__ == '__main__':
#     unittest.main()