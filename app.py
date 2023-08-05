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

        return jsonify({"error": "restaurant not found"}),404
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

        # Scenario 6: no query, no lon but lat exist OR no query, no lat but lon exist--> return default lat, lon and ask for lat, lon, error 400 Bad Request
        elif (lat_param is None and lon_param is not None) or (lat_param is not None and lon_param is None):
            return jsonify({
                "lat": default_lat,
                "lon": default_lon,
                "error": "Please provide both latitude and longitude for accurate results"
            }), 400
        # Scenario 7: no query, no lat, lon exits —> return default location and ask for query, error 400 Bad Request
        else:
            return jsonify({
                "lat": default_lat,
                "lon": default_lon,
                "error": "Please provide a query to get the restaurant recommendations"
            }), 400


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


# def check_current_location(query):
#     # query = request.args.get("q", "")
#     default_lat = 60.170456
#     default_lon = 24.9383042
#     current_lat = 0
#     current_lon = 0
#     results = []

#     lat_param = request.args.get("lat")
#     lon_param = request.args.get("lon")

#     # Better solution
#     if lat_param is not None and lon_param is not None:
#         try:
#             current_lat = lat_param
#             current_lon = lon_param
#         except ValueError:
#             return jsonify({"error": "Invalid lattitude or longitude values"})
#     else:
#         current_lat = default_lat
#         current_lon = default_lon
#         # current_lat = float(request.args.get("lat", default_lat))
#         # current_lon = float(request.args.get("lon", default_lon))

#     # Simple Solution:
#     # if lat_param is not None and lon_param is not None:
#     #     # if latitude and longitude parameters are present, update the current values
#     #     current_lat = float(lat_param)
#     #     current_lon = float(long_param)
#     # elif lat_param is None and lon_param is None:
#     #     current_lat = float(request.args.get("lat", default_lat))
#     #     current_lon = float(request.args.get("lon", default_lon))
#     # else:
#     #     print("Error: Invalid latitude or longitude values.")

#     for restaurant in restaurants:
#         distance = calculate_distance(
#             current_lat, current_lon, restaurant["location"][1], restaurant["location"][0])

#         if distance is not None and distance <= 3 and query.lower() in restaurant["name"].lower():

#             results.append({
#                 "name": restaurant["name"],
#                 "city": restaurant["city"],
#                 "currency": restaurant["currency"],
#                 "delivery_price": restaurant["delivery_price"],
#                 "description": restaurant["description"],
#                 "tags": restaurant["tags"],
#                 "distance": distance if distance is not None else None,
#             })

#         if len(results) > 0:
#             return jsonify(results)
#         else:
#             return jsonify({"message": "No matching restaurant found"})
