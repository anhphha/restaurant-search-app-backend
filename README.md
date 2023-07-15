# restaurant-search-app-backend


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