from flask import Flask, jsonify, request
import math

APP = Flask(__name__)

# Sample restaurant data
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
    }
]


@APP.route('/', methods=['GET'])
def helloworld():
    if(request.method == 'GET'):
        data = {"data": "Hello World"}
        return jsonify(data)

@APP.route("/restaurants", methods=["GET"])
def search_restaurants():
    query = request.args.get("q", "")
    lat = float(request.args.get("lat", 0))
    lon = float(request.args.get("lon", 0))

    results = []

    for restaurant in restaurants:
        distance = calculate_distance(
            lat, lon, restaurant["location"][1], restaurant["location"][0])

        if distance <= 3 and query.lower() in restaurant["name"].lower():
            results.append(restaurant)

    return jsonify(results)


def calculate_distance(lat1, lon1, lat2, lon2):
    # This is a simple implementation of the haversine formula to calculate the distance between two coordinates
    radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)*math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance=radius * c
    return distance


if __name__ == "__main__":
    app.run()
