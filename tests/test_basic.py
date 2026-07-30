from src import create_app


def test_create_app():
    # Create a new Flask application instance
    app = create_app()

    # Verify that the app was created successfully
    assert app is not None