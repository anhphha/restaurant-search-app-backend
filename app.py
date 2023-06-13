from flask import Flask, jsonify, request
import math
import re

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
    if (request.method == 'GET'):
        data = {"data": "Hello World"}
        return jsonify(data)


@APP.route("/restaurants", methods=["GET"])
def get_restaurant():
    return jsonify(restaurants)


@APP.route("/restaurants/search", methods=["GET"])
def get_restaurant_info():
    query = request.args.get("q", "")
    lat_param = request.args.get("lat")
    lon_param = request.args.get("lon")
    if query:
        for restaurant in restaurants:
            if (query.lower() in restaurant["name"].lower()
                or query.lower() in restaurant["description"].lower()
                    or query.lower() in restaurant["tag"].lower()):
                # scenario 1: if there is query (name, description, tag) but no lat, lon --> return return restaurant info
                if lat_param is None and lon_param is None:
                    return  jsonify({
                        "name": restaurants[0]["name"],
                        "city": restaurants[0]["city"],
                        "currency": restaurants[0]["currency"],
                        "delivery_price": restaurants[0]["delivery_price"],
                        "description": restaurants[0]["description"],
                        "tags": restaurants[0]["tags"]
                    })

                # scenario 2: if there is query, latitude, longitude, then return restaurant name + distance
                elif lat_param is not None and lon_param is not None:
                    distance = calculate_distance(
                        float(lat_param), float(lon_param), restaurant["location"][1], restaurant["location"][0])

                    restaurant_info = {
                        "name": restaurants[0]["name"],
                        "city": restaurants[0]["city"],
                        "currency": restaurants[0]["currency"],
                        "delivery_price": restaurants[0]["delivery_price"],
                        "description": restaurants[0]["description"],
                        "tags": restaurants[0]["tags"],
                        "distance": distance if distance is not None else None,
                    }

                    return jsonify(restaurant_info)

        return jsonify({"message": "restaurant not found"})
    else:
        # return jsonify({"message": "Please provide a restaurant in the query"})
        return check_current_location("momo")

    # tra error 404


def check_current_location(query):
    # query = request.args.get("q", "")
    print(query)
    default_lat = 60.170456
    default_lon = 24.9383042
    current_lat = 0
    current_lon = 0
    results = []

    lat_param = request.args.get("lat")
    lon_param = request.args.get("long")

    # Better solution
    if lat_param is not None and lon_param is not None:
        try:
            current_lat = lat_param
            current_lon = lon_param
        except ValueError:
            return jsonify({"error": "Invalid lattitude or longitude values"})
    else:
        current_lat = default_lat
        current_lon = default_lon
        # current_lat = float(request.args.get("lat", default_lat))
        # current_lon = float(request.args.get("lon", default_lon))

    # Simple Solution:
    # if lat_param is not None and lon_param is not None:
    #     # if lattitude and longitude parameters are present, update the current values
    #     current_lat = float(lat_param)
    #     current_lon = float(long_param)
    # elif lat_param is None and lon_param is None:
    #     current_lat = float(request.args.get("lat", default_lat))
    #     current_lon = float(request.args.get("lon", default_lon))
    # else:
    #     print("Error: Invalid latitude or longitude values.")

    for restaurant in restaurants:
        distance = calculate_distance(
            current_lat, current_lon, restaurant["location"][1], restaurant["location"][0])

        if distance <= 3 and query.lower() in restaurant["name"].lower():
            results.append(restaurant)

    return jsonify({
        "name": results[0]["name"],
        "city": results[0]["city"],
        "currency": results[0]["currency"],
        "delivery_price": results[0]["delivery_price"],
        "description": results[0]["description"]
    })


def calculate_distance(lat1, lon1, lat2, lon2):
    # This is a simple implementation of the haversine formula to calculate the distance between two coordinates
    radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * \
        math.cos(math.radians(lat2)) * math.sin(dlon/2)*math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = radius * c
    print(distance)
    return distance


if __name__ == "__main__":
    app.run()
