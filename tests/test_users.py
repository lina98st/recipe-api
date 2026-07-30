from src.api.users import scramble
from src import create_app

def test_password_scramble():
    # Create a sample password for testing
    password = "qVk*fv:}7LUEcVa7m"

    # Hash the password using the scramble function
    hashed_password = scramble(password)

    # Verify that the hashed password is different from the original password
    assert password != hashed_password


def test_random_salt():
    # Create a sample password for testing
    password = "AKzX@Jv_tE2B,maJQ"

    # Generate two hashes from the same password
    hashed_password = scramble(password)
    hashed_password2 = scramble(password)

    # Verify that a new random salt creates a different hash each time
    assert hashed_password != hashed_password2


def test_get_users():
    # Create a new Flask application instance
    app = create_app()

    # Create a test client for sending HTTP requests
    client = app.test_client()

    # Send a GET request to the /users endpoint
    response = client.get("/users")

    # Verify that the request was successful
    assert response.status_code == 200



def test_get_user_not_found():
    # Create a new Flask application instance
    app = create_app()

    # Create a test client for sending HTTP requests
    client = app.test_client()

    # Send a GET request with a non-existing user ID
    response = client.get("/users/999999")

    # Verify that the API returns 404 Not Found
    assert response.status_code == 404


def test_missing_user_fields():
    # Create a new Flask application instance
    app = create_app()

    # Create a test client for sending HTTP requests
    client = app.test_client()

    # Send a POST request with an empty JSON body
    response = client.post("/users", json={})

    # Verify that the request fails because required fields are missing
    assert response.status_code == 400

