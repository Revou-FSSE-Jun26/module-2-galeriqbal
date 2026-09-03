from models import db, Product, Order, order_items


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def seed_product(app, name="Blade of Despair", price=10000, stock=25):
    """Insert a product directly into the test database and return its id."""
    with app.app_context():
        product = Product(name=name, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return product.id


def seed_order_with_product(app, product_id):
    """Create an order linked to a product (used for the delete-guard test)."""
    with app.app_context():
        order = Order(user_id=1, total_prices=10000)
        db.session.add(order)
        db.session.flush()
        db.session.execute(order_items.insert().values(
            order_id=order.id,
            product_id=product_id,
            quantity=1,
            product_price=10000,
        ))
        db.session.commit()


# ---------- GET /products ----------

def test_get_all_products_empty(client):
    response = client.get("/products")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_all_products_with_data(client, app):
    seed_product(app, "Blade of Despair")
    seed_product(app, "Holy Crystal")

    response = client.get("/products")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2


# ---------- GET /products/<id> ----------

def test_get_product_by_id(client, app):
    product_id = seed_product(app, "Blade of Despair")

    response = client.get(f"/products/{product_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["name"] == "Blade of Despair"


def test_get_product_not_found(client):
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


# ---------- POST /products ----------

def test_create_product(client, auth_token):
    response = client.post(
        "/products",
        json={"name": "New Item", "price": 5000, "stock": 10},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["name"] == "New Item"


def test_create_product_missing_name(client, auth_token):
    response = client.post(
        "/products",
        json={"price": 5000, "stock": 10},
        headers=auth_header(auth_token),
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "name is required"


def test_create_product_negative_price(client, auth_token):
    response = client.post(
        "/products",
        json={"name": "Bad Item", "price": -100, "stock": 10},
        headers=auth_header(auth_token),
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "price must be a positive number"


def test_create_product_no_token(client):
    response = client.post("/products", json={"name": "X", "price": 1, "stock": 1})
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token is missing"


# ---------- PUT /products/<id> ----------

def test_update_product(client, app, auth_token):
    product_id = seed_product(app, "Old Name")

    response = client.put(
        f"/products/{product_id}",
        json={"price": 20000},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["price"] == 20000


def test_update_product_not_found(client, auth_token):
    response = client.put(
        "/products/999",
        json={"price": 20000},
        headers=auth_header(auth_token),
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


def test_update_product_negative_stock(client, app, auth_token):
    product_id = seed_product(app, "Item")

    response = client.put(
        f"/products/{product_id}",
        json={"stock": -5},
        headers=auth_header(auth_token),
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "stock must be a positive number"


# ---------- DELETE /products/<id> ----------

def test_delete_product(client, app, auth_token):
    product_id = seed_product(app, "To Delete")

    response = client.delete(
        f"/products/{product_id}",
        headers=auth_header(auth_token),
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Product deleted successfully"


def test_delete_product_not_found(client, auth_token):
    response = client.delete("/products/999", headers=auth_header(auth_token))
    assert response.status_code == 404
    assert response.get_json()["error"] == "Product not found"


def test_delete_product_with_active_orders(client, app, auth_token):
    """Error case: cannot delete a product that is linked to an order."""
    product_id = seed_product(app, "Locked Item")
    seed_order_with_product(app, product_id)

    response = client.delete(
        f"/products/{product_id}",
        headers=auth_header(auth_token),
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "Cannot delete product with active orders"
