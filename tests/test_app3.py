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


@app.route("/restaurants/search", methods=["GET"])
def get_restaurant_info():
    query = request.args.get("q", "")
    lat_param = request.args.get("lat")
    lon_param = request.args.get("lon")
    default_lat = 60.170456
    default_lon = 24.9383042

    if query:
        matching_restaurants = []

        for restaurant in restaurants:

            restaurant_info = {
                "name": restaurant["name"],
                "city": restaurant["city"],
                "currency": restaurant["currency"],
                "delivery_price": restaurant["delivery_price"],
                "description": restaurant["description"],
                "tags": restaurant["tags"],
            }

            if (query.lower() in restaurant["name"].lower()
                or query.lower() in restaurant["description"].lower()
                    or query.lower() in [tag.lower() for tag in restaurant["tags"]]):

                # scenario 1: if there is query (name, description, tag) but no lat, lon --> return restaurant (objects) which match the given query string and are closer than 3 kilometers from coordinates.
                if lat_param is None and lon_param is None:
                    # return check_current_location(query)
                    matching_restaurants.append(restaurant_info)
                    # ---> this return only the restaurant info and ignore the distance
                    return jsonify(matching_restaurants)

                # scenario 2: if there is query, latitude, longitude, then return restaurant info + distance
                elif lat_param is not None and lon_param is not None:
                    distance = calculate_distance(
                        float(lat_param), float(lon_param), restaurant["location"][1], restaurant["location"][0])

                    restaurant_info_with_distance = {
                        "name": restaurant["name"],
                        "city": restaurant["city"],
                        "currency": restaurant["currency"],
                        "delivery_price": restaurant["delivery_price"],
                        "description": restaurant["description"],
                        "tags": restaurant["tags"],
                        "distance": distance if distance is not None else None,
                    }

                    matching_restaurants.append(restaurant_info)

                    return jsonify(matching_restaurants)

                # scenario 3: if there is query, latitude, but no longitude, then return restaurant info only
                elif lat_param is not None and lon_param is None:
                    matching_restaurants.append(restaurant_info)
                    return jsonify(matching_restaurants)

                # scenario 4: if there is query, longitude, but no latitude, then return restaurant info only
                elif lat_param is None and lon_param is not None:
                    matching_restaurants.append(restaurant_info)
                    return jsonify(matching_restaurants)

        return jsonify({"message": "restaurant not found"})
    else:
        # Scenario 5: no query but lat, lon exist --> return location and restaurant recommendations within 3 km
        if lat_param is not None and lon_param is not None:
            nearby_restaurants = []

            for restaurant in restaurants:
                distance = calculate_distance(
                    float(lat_param), float(lon_param), restaurant["location"][1], restaurant["location"][0])

                if distance is not None and distance <= 3.0:  # Filter restaurants with distance <=3.0
                    nearby_restaurants.append({
                        "name": restaurant["name"],
                        "city": restaurant["city"],
                        "currency": restaurant["currency"],
                        "delivery_price": restaurant["delivery_price"],
                        "description": restaurant["description"],
                        "tags": restaurant["tags"],
                        "distance": distance if distance is not None else None,
                    })

            return jsonify({
                "current latitude": lat_param,
                "current longitude": lon_param,
                "nearby_restaurant": nearby_restaurants,
            })

        # Scenario 6: no query, no lon but lat exist OR no query, no lat but lon exist--> return default lat, lon and ask for lat, lon
        elif (lat_param is None and lon_param is not None) or (lat_param is not None and lon_param is None):
            return jsonify({
                "lat": default_lat,
                "lon": default_lon,
                "message": "Please provide both latitude and longitude for accurate results"
            })
        # Scenario 7: no query, lat, lon exits —> return default location and ask for query
        else:
            return jsonify({
                "lat": default_lat,
                "lon": default_lon,
                "message": "Please provide a query to get the restaurant recommendations"
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


def test_get_restaurant_info_with_query():
    response = client.get('/restaurants/search?q=momo')
    assert response.status_code == 200
    assert response.json == [
        {
            "name": "Momotoko Citycenter",
            "city": "Helsinki",
            "currency": "EUR",
            "delivery_price": 390,
            "description": "Japanese ramen at its best",
            "tags": ["ramen", "risotto"],
        }
    ]


def test_get_restaurant_info_without_query():
    response = client.get('/restaurants/search')
    assert response.status_code == 200
    assert response.json == {
        "lat": 60.170456,
        "lon": 24.9383042,
        "message": "Please provide a query to get the restaurant recommendations"
    }

if __name__ == "__main__":
    pytest.main()