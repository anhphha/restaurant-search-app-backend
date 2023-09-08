from flask import Flask, request, jsonify
from flask.testing import FlaskClient


# Create a test client
app = Flask(__name__)
client = app.test_client()


restaurants = [
    {
        "city": "Helsinki",
        "currency": "EUR",
        "delivery_price": 390,
        "description": "Japanese ramen at its best",
        "image": "https://prod-wolt-venue-images-cdn.wolt.com/5d108aa82e757db3f4946ca9/d88ebd36611a5e56bfc6a60264fe3f81",
        "location": [24.941786527633663, 60.169934599421396],
        "name": "Momotoko Citycenter",
        "online": False,
        "tags": ["ramen", "risotto"],
        "blurhash": "j2DUFG8jbu8AXuLIT5Tt0B01R2;;"
    }
]

@app.route("/restaurants", methods=["GET"])
def get_restaurant():
    return jsonify(restaurants)

def test_get_restaurant():
    response = client.get('/restaurants')
    assert response.status_code == 200
    assert response.json == restaurants

if __name__ == "__main__":
    pytest.main()