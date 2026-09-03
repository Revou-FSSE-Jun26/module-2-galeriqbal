from models import db, Category


def auth_header(token):
    """Helper to build the Authorization header for protected routes."""
    return {"Authorization": f"Bearer {token}"}


def seed_category(app, name="PHYSICAL"):
    """Insert a category directly into the test database and return its id."""
    with app.app_context():
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return category.id


# ---------- GET /categories ----------

def test_get_all_categories_empty(client):
    """Happy path: returns an empty list when there are no categories."""
    response = client.get("/categories")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_all_categories_with_data(client, app):
    """Happy path: returns all categories."""
    seed_category(app, "PHYSICAL")
    seed_category(app, "MAGIC")

    response = client.get("/categories")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "PHYSICAL"


# ---------- GET /categories/<id> ----------

def test_get_category_by_id(client, app):
    """Happy path: returns a single category by id."""
    category_id = seed_category(app, "MAGIC")

    response = client.get(f"/categories/{category_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == category_id
    assert data["name"] == "MAGIC"


def test_get_category_not_found(client):
    """Error case: returns 404 when the category does not exist."""
    response = client.get("/categories/999")
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Category not found"


# ---------- POST /categories ----------

def test_create_category(client, auth_token):
    """Happy path: creates a category with valid data and a valid token."""
    response = client.post(
        "/categories",
        json={"name": "DEFENSE"},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["name"] == "DEFENSE"
    assert "id" in data


def test_create_category_missing_name(client, auth_token):
    """Error case: returns 400 when name is missing."""
    response = client.post(
        "/categories",
        json={},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "name is required"


def test_create_category_no_token(client):
    """Error case: returns 401 when no token is provided."""
    response = client.post("/categories", json={"name": "DEFENSE"})
    data = response.get_json()

    assert response.status_code == 401
    assert data["error"] == "Token is missing"


# ---------- PUT /categories/<id> ----------

def test_update_category(client, app, auth_token):
    """Happy path: updates an existing category."""
    category_id = seed_category(app, "OLD NAME")

    response = client.put(
        f"/categories/{category_id}",
        json={"name": "NEW NAME"},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "NEW NAME"


def test_update_category_not_found(client, auth_token):
    """Error case: returns 404 when updating a non-existent category."""
    response = client.put(
        "/categories/999",
        json={"name": "NEW NAME"},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Category not found"


def test_update_category_missing_name(client, app, auth_token):
    """Error case: returns 400 when name is missing on update."""
    category_id = seed_category(app, "SOME NAME")

    response = client.put(
        f"/categories/{category_id}",
        json={},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"] == "name is required"


# ---------- DELETE /categories/<id> ----------

def test_delete_category(client, app, auth_token):
    """Happy path: deletes an existing category."""
    category_id = seed_category(app, "TO DELETE")

    response = client.delete(
        f"/categories/{category_id}",
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["message"] == "Category deleted successfully"


def test_delete_category_not_found(client, auth_token):
    """Error case: returns 404 when deleting a non-existent category."""
    response = client.delete(
        "/categories/999",
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 404
    assert data["error"] == "Category not found"
