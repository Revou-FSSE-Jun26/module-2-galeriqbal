import os
import pytest
import jwt
from datetime import datetime, timedelta, timezone
from werkzeug.security import generate_password_hash

from app import create_app
from models import db, User


@pytest.fixture
def app():
    """Create a Flask app configured for testing with an in-memory SQLite DB."""
    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }

    app = create_app(test_config)

    # Create all tables in the fresh in-memory database
    with app.app_context():
        db.create_all()
        yield app
        # Teardown: drop everything after the test finishes
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client used to send requests to the app without running a server."""
    return app.test_client()


@pytest.fixture
def auth_token(app):
    """Create a test user and return a valid JWT token for authenticated requests."""
    with app.app_context():
        user = User(
            name="baalzebub",
            email="baalzebub@example.com",
            password_hash=generate_password_hash("admin123789"),
            role="admin",
        )
        db.session.add(user)
        db.session.commit()

        token = jwt.encode(
            {
                "user_id": user.id,
                "email": user.email,
                "exp": datetime.now(timezone.utc) + timedelta(hours=1),
            },
            os.getenv("JWT_SECRET_KEY"),
            algorithm="HS256",
        )

    return token
