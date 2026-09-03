from werkzeug.security import generate_password_hash
from models import db, User


def seed_user(app, email="login@example.com", password="password123"):
    """Insert a user with a hashed password so login can be tested."""
    with app.app_context():
        user = User(
            name="Login User",
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        return user.id


# ---------- POST /register ----------

def test_register_user(client):
    response = client.post(
        "/register",
        json={"name": "New User", "email": "new@example.com", "password": "secret123"},
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "User registered successfully"
    assert data["user"]["email"] == "new@example.com"


def test_register_missing_fields(client):
    response = client.post("/register", json={"name": "No Email"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "name, email, and password are required"


# ---------- GET /users/<id> ----------

def test_get_user_by_id(client, app):
    user_id = seed_user(app, "getme@example.com")

    response = client.get(f"/users/{user_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["email"] == "getme@example.com"


def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "User not found"


# ---------- POST /auth/login ----------

def test_login_success(client, app):
    seed_user(app, "login@example.com", "password123")

    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Login successful"
    assert "token" in data


def test_login_wrong_password(client, app):
    seed_user(app, "login@example.com", "password123")

    response = client.post(
        "/auth/login",
        json={"email": "login@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid email or password"


def test_login_missing_fields(client):
    response = client.post("/auth/login", json={"email": "login@example.com"})
    assert response.status_code == 400
    assert response.get_json()["error"] == "email and password are required"


def test_login_user_not_found(client):
    response = client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )
    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid email or password"
