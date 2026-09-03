from models import db, Order, Product, order_items


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def seed_product(app, name="Blade of Despair", price=10000, stock=25):
    with app.app_context():
        product = Product(name=name, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return product.id


def seed_order(app, user_id=1, total_prices=10000):
    with app.app_context():
        order = Order(user_id=user_id, total_prices=total_prices)
        db.session.add(order)
        db.session.commit()
        return order.id


# ---------- GET /orders ----------

def test_get_all_orders_empty(client):
    response = client.get("/orders")
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_all_orders_with_data(client, app):
    seed_order(app)
    seed_order(app)

    response = client.get("/orders")
    data = response.get_json()

    assert response.status_code == 200
    assert len(data) == 2


# ---------- GET /orders/<id> ----------

def test_get_order_by_id(client, app):
    order_id = seed_order(app, total_prices=15000)

    response = client.get(f"/orders/{order_id}")
    data = response.get_json()

    assert response.status_code == 200
    assert data["id"] == order_id
    assert "products" in data


def test_get_order_not_found(client):
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert response.get_json()["error"] == "Order not found"


# ---------- POST /orders ----------

def test_create_order(client, app, auth_token):
    product_id = seed_product(app, "Blade of Despair")

    response = client.post(
        "/orders",
        json={
            "user_id": 1,
            "total_prices": 10000,
            "products": [
                {"product_id": product_id, "quantity": 1, "product_price": 10000}
            ],
        },
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Order created successfully"
    assert product_id in data["products_linked"]


def test_create_order_missing_user_id(client, auth_token):
    response = client.post(
        "/orders",
        json={"products": [{"product_id": 1, "quantity": 1}]},
        headers=auth_header(auth_token),
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "user_id is required"


def test_create_order_missing_products(client, auth_token):
    response = client.post(
        "/orders",
        json={"user_id": 1},
        headers=auth_header(auth_token),
    )
    assert response.status_code == 400
    assert response.get_json()["error"] == "products list is required"


def test_create_order_no_token(client):
    response = client.post("/orders", json={"user_id": 1, "products": []})
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token is missing"


# ---------- PUT /orders/<id> ----------

def test_update_order(client, app, auth_token):
    order_id = seed_order(app, total_prices=10000)

    response = client.put(
        f"/orders/{order_id}",
        json={"total_prices": 99999},
        headers=auth_header(auth_token),
    )
    data = response.get_json()

    assert response.status_code == 200
    assert data["total_prices"] == 99999


def test_update_order_not_found(client, auth_token):
    response = client.put(
        "/orders/999",
        json={"total_prices": 99999},
        headers=auth_header(auth_token),
    )
    assert response.status_code == 404
    assert response.get_json()["error"] == "Order not found"


# ---------- DELETE /orders/<id> ----------

def test_delete_order(client, app, auth_token):
    order_id = seed_order(app)

    response = client.delete(
        f"/orders/{order_id}",
        headers=auth_header(auth_token),
    )
    assert response.status_code == 200
    assert response.get_json()["message"] == "Order deleted successfully"


def test_delete_order_not_found(client, auth_token):
    response = client.delete("/orders/999", headers=auth_header(auth_token))
    assert response.status_code == 404
    assert response.get_json()["error"] == "Order not found"
