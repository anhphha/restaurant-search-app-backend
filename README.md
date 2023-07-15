# Restaurant Search App Backend

### This is a assignment for WOLT Programme.

### Created and made by Anh Ha

## Overview
A list of restaurants is an important element in Wolt app. Depending on where our customers are located, they will be able to order food from few dozen or even from hundreds of different restaurants. Views in the app (Discovery, Search, Delivers, Nearby) sort restaurants based on the delivery time, popularity, rating and various other factors when trying to find the most relevant matches for each customer.

## Restaurant data
```restaurant.json``` contains fifty restaurants from central Helsinki area. Each object has a set fields providing more information about the restaurant, like name, image and location.

Example:
```
{
    "city": "Helsinki",
    "currency": "EUR",
    "delivery_price": 390,
    "description": "Japanilaista ramenia parhaimmillaan",
    "image": "https://prod-wolt-venue-images-cdn.wolt.com/5d108aa82e757db3f4946ca9/d88ebd36611a5e56bfc6a60264fe3f81",
    "location": [
        24.941786527633663,
        60.169934599421396
    ],
    "name": "Momotoko Citycenter",
    "online": false,
    "tags": [
        "ramen",
        "risotto"
    ],
    "blurhash": "j2DUFG8jbu8AXuLIT5Tt0B01R2;;",
}
```

Fields:

- City : A city where the restaurant is located (type: string)
- Currency: ISO 4217 code of the currency the restaurant is using (type: string)
_ Delivery price: Delivery cost from the restaurant to a customer. The price is stored as subunits, so 390 in this case would be 3.90€ (type: integer)
- Description: More information about what kind of restaurant it is (type: string)
- Image: A link to restaurant's image (type: string)
- Location: Restaurant's location in latitude & longitude coordinates. First element in the list is the longitude (type: a list containing two decimal elements)
- Name: The name of the restaurant (type: string)
- Online: If true, the restaurant is accepting orders at the moment. If false, then ordering is not possible (type: boolean)
- Tags: A list of tags describing what kind of food the restaurant sells, e.g. pizza / burger (type: a list of strings, max. 3 elements)
- Blurhash : See bonus task

## Backend task - search
Create a REST API endpoint that allows searching restaurants. API needs to accept three parameters:

- q: query string. Full or partial match for the string is searched from name, description and tags fields. A minimum length for the query string is one character.
- lat: latitude coordinate (customer's location)
- lon : longitude coordinate (customer's location)
API should return restaurant (objects) which match the given query string and are closer than 3 kilometers from coordinates.

Example query:
```
/restaurants/search?q=sushi&lat=60.17045&lon=24.93147
```
This search would return restaurants (in JSON format) which contain a word sushi and are closer than 3km to the point [60.17045, 24.93147].

Please do not use any on-disk database (MySQL, PostgreSQL, ...) or ElasticSearch in this assignment. The task can be completed without them.

## Bonus task: Blurhash
Restaurant data also includes a field called blurhash. As a bonus task you can figure out what this field is and use it:

- In frontend task you can render the blurhash data
- In backend task you can e.g. validate that blurhash-field is correct when loading data from restaurant.json

There are some ready-made libraries for manipulating blurhash values. Feel free use those or create your own one.

Bonus task is completely optional and it doesn't affect how we review assignments. It exists only for fun! 😀

## Few tips
- Everyone in Wolt loves clean code
- Everyone in Wolt also loves good tests
- Try to figure out what is the essential part in this task. Focus on that first.
- Don't forget README.md with clear instructions how to get the project up and running

# TESTING FLASK FRAMEWORK WITH PYTEST
## Installation

```
python -m venv venv
virtualenv flask
source venv/bin/activate
pip install pytest
pip freeze > requirements.txt
pip install -r requirements.txt
```
## Running the Application

```
FLASK_APP=api.py flask run`
```

## Execution all the Tests

To execute all the tests, run the following command:
```
pytest
```

## Execution all the Tests with stdout response

To execute all the tests, run the following command:
```
pytest -s
```

## Executing only grouped Tests

To only execute the get_request grouped tests, run the following command:
```
pytest -m get_request
```
# Details

This repo is built following a tutorial published on CircleCI blog under the CircleCI Guest Writer Program.

Blog post: [Testing Flask Framework with Pytest](https://circleci.com/blog/testing-flask-framework-with-pytest/)