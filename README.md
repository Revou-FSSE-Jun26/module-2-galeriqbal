# RevoShop API

Flask REST API with PostgreSQL for managing products, users, and orders.

## Overview

RevoShop is a backend REST API for a simple e-commerce store. It manages users, product categories, products, and orders, including a many-to-many relationship between orders and products. The API supports full CRUD operations, JWT-based authentication, data validation, and error handling.

## Features Implemented

- Full CRUD for **products**, **categories**, and **orders**
- Many-to-many relationship between orders and products through the `order_items` association table
- User registration and JWT-based login (`/auth/login`)
- Protected routes (POST/PUT/DELETE) that require a valid JWT token
- Data validation on product creation and update (name, price, stock)
- Error handling with meaningful messages and proper HTTP status codes
- Deletion guard that blocks removing a product that is still linked to active orders
- Sensitive config (database URL, secret key, debug mode) loaded from `.env`
- Automated tests with pytest and load testing with Locust

## Requirements

- Python 3.x
- PostgreSQL
- pgAdmin / DBeaver
- Postman (for API testing)

## How To Run

### 1. Clone repository

```bash
git clone https://github.com/Revou-FSSE-Jun26/module-2-galeriqbal.git
cd module-2-galeriqbal
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup environment variables

Copy `.env.example` to `.env` and fill in your own values:

```bash
cp .env.example .env
```

`.env` contains:

```
DATABASE_URL=postgresql://username:password@localhost/revoshop_db
JWT_SECRET_KEY=your_secret_key_here
FLASK_DEBUG=True
```

### 5. Setup database

Create a `revoshop_db` database in PostgreSQL, then run the SQL files:

```bash
psql -U postgres -d revoshop_db -f revoshop_db/schema.sql
psql -U postgres -d revoshop_db -f revoshop_db/seed.sql
psql -U postgres -d revoshop_db -f revoshop_db/queries.sql
```

### 6. Run migrations

```bash
flask db upgrade
```

### 7. Run the app

```bash
python app.py
```

Server runs at `http://localhost:5000`

## Database Schema

![Database Schema](revoshop_db/assets/schema_diagram.png)

### Tables

| Table | Description |
|-------|-------------|
| users | User data with role column |
| categories | Product categories |
| products | Product data, FK to categories |
| orders | Order data, FK to users |
| order_items | Association table (many-to-many) between orders and products |

## API Endpoints

### GET /

Health check.

**Response:**
```json
{"message": "Flask is connected to PostgreSQL!", "status": "ok"}
```

---

### POST /register

Register a new user.

![Register User](revoshop_db/assets/register_users.png)

**Request Body:**
```json
{
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123"
}
```

**Response (201):**
```json
{
    "message": "User registered successfully",
    "user": {
        "id": 21,
        "name": "Test User",
        "email": "test@example.com"
    }
}
```

---

### GET /users/:id

Retrieve a user by ID.

**Response (200):**
```json
{
    "id": 1,
    "name": "Johan Liebert",
    "email": "johan.liebert@example.com",
    "created_at": "2026-08-12T10:00:00+00:00"
}
```

**Response (404):**
```json
{"error": "User not found"}
```

---

### GET /products

Retrieve all products (hardcoded).

**Response (200):** Array of 20 products.

---

### GET /products/:id

Retrieve a product by ID.

**Response (200):**
```json
{
    "id": 1,
    "categories_id": 1,
    "name": "Blade of Despair",
    "price": 10000,
    "stock": 25,
    "description": "Physical Attack tinggi dengan bonus damage saat musuh HP rendah."
}
```

**Response (404):**
```json
{"error": "Product not found"}
```

---

### POST /seed-order

Insert a sample order linked to multiple products (many-to-many demo).

**Response (201):**
```json
{
    "message": "Order created with multiple products (many-to-many)",
    "order_id": 21,
    "products_linked": [1, 6, 18]
}
```

---

### GET /orders/:id

Retrieve an order with its linked products (many-to-many).

**Response (200):**
```json
{
    "order_id": 21,
    "user_id": 1,
    "total_prices": 25500.0,
    "products": [
        {"product_id": 1, "quantity": 1, "product_price": 10000.0},
        {"product_id": 6, "quantity": 1, "product_price": 25000.0},
        {"product_id": 18, "quantity": 1, "product_price": 2400.0}
    ]
}
```

**Response (404):**
```json
{"error": "Order not found"}
```

---

### POST /auth/login

Log in and receive a JWT token. Use this token in the `Authorization: Bearer <token>` header for protected routes.

**Request Body:**
```json
{
    "email": "test@example.com",
    "password": "password123"
}
```

**Response (200):**
```json
{
    "message": "Login successful",
    "token": "eyJhbGciOiJIUzI1NiIs...",
    "user": {
        "id": 21,
        "name": "Test User",
        "email": "test@example.com",
        "role": "user"
    }
}
```

**Response (401):**
```json
{"error": "Invalid email or password"}
```

---

### POST /products (protected)

Create a new product. Requires a valid JWT token.

**Request Body:**
```json
{
    "name": "New Item",
    "price": 5000,
    "stock": 10,
    "categories_id": 1,
    "description": "A new item"
}
```

**Response (201):** the created product.

**Response (400):** validation error, e.g.
```json
{"error": "price must be a positive number"}
```

---

### PUT /products/:id (protected)

Update an existing product. Requires a valid JWT token and passes the same validation as creation.

**Response (200):** the updated product.
**Response (404):** `{"error": "Product not found"}`

---

### DELETE /products/:id (protected)

Delete a product. Blocked if the product is still linked to active orders.

**Response (200):** `{"message": "Product deleted successfully"}`
**Response (400):** `{"error": "Cannot delete product with active orders"}`

---

### GET /categories

Retrieve all categories.

### GET /categories/:id

Retrieve a single category by ID. Returns 404 if not found.

### POST /categories (protected)

Create a new category.

**Request Body:**
```json
{"name": "NEW CATEGORY"}
```

### PUT /categories/:id (protected)

Update a category.

### DELETE /categories/:id (protected)

Delete a category.

---

### GET /orders

Retrieve all orders.

### POST /orders (protected)

Create a new order linked to multiple products (many-to-many).

**Request Body:**
```json
{
    "user_id": 1,
    "total_prices": 17500,
    "products": [
        {"product_id": 1, "quantity": 1, "product_price": 10000},
        {"product_id": 3, "quantity": 1, "product_price": 7500}
    ]
}
```

### PUT /orders/:id (protected)

Update an existing order.

### DELETE /orders/:id (protected)

Delete an order.

## Postman Documentation

Full API documentation with examples: [Postman Documentation](https://documenter.getpostman.com/view/57336663/2sBYApxsdU)

### Screenshots

**GET request**

![GET request](revoshop_db/assets/postman_get.png)

**POST request**

![POST request](revoshop_db/assets/postman_post.png)

**PUT request**

![PUT request](revoshop_db/assets/postman_put.png)

**DELETE request**

![DELETE request](revoshop_db/assets/postman_delete.png)

**pgAdmin tables**

![pgAdmin tables](revoshop_db/assets/pgadmin_tables.png)

## Migration

The `role` column was added to the `users` table using Flask-Migrate:

![Add Role to Users](revoshop_db/assets/add_roles_to_users.png)

```bash
flask db migrate -m "add role column to users"
flask db upgrade
```

Migration file: `migrations/versions/83c2828fa2e1_add_role_coloumn_to_users.py`

## Testing (pytest)

Automated tests cover all CRUD endpoints for categories, products, orders, and auth, including both happy path and error cases. Tests use an in-memory SQLite database so they do not touch the real PostgreSQL data.

Run all tests:

```bash
python -m pytest -v
```

## Load Testing (Locust)

The `locustfile.py` simulates a sequential user journey: GET all products, GET a single product by ID, POST a new order, and GET the created order.

Run Locust (with the app running in another terminal):

```bash
locust -f locustfile.py --host http://localhost:5000
```

Then open `http://localhost:8089` and start with 50 users, gradually increasing to 200 users.

![Locust 200 users](revoshop_db/assets/locust_200users.png)

## Tech Stack

- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- PostgreSQL
- pgAdmin
- psycopg2-binary
- python-dotenv
- PyJWT
- pytest
- Locust

Thank you.
