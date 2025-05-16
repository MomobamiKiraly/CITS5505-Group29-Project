import pytest
from app import create_app
from app import create_app, db 

# Fixture to create and configure a new app instance for each test
@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,                # Enable testing mode
        "WTF_CSRF_ENABLED": False,      # Disable CSRF protection for testing
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"  # Use in-memory SQLite database
    })

    with app.app_context():
        db.create_all()  # Create all database tables

    yield app  # Provide the app to the test

# Fixture to create a test client for the app
@pytest.fixture
def client(app):
    return app.test_client()