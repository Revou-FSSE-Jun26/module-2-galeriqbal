from locust import HttpUser, task, between


class RevoShopUser(HttpUser):
    """
    Simulates a user journey against the RevoShop API:
      1. GET all products
      2. GET a single product by ID
      3. POST a new order
      4. GET the created order

    Run:
      locust -f locustfile.py --host http://localhost:5000
    Then open http://localhost:8089 and set:
      - Number of users: 200
      - Ramp up: start at 50, spawn rate to grow toward 200
    """

    # Wait 1-3 seconds between each task cycle to mimic real user behaviour
    wait_time = between(1, 3)

    def on_start(self):
        """Runs once per simulated user: register + login to obtain a JWT token."""
        # Use a unique email per user so registration does not collide
        unique = self.environment.runner.user_count if self.environment.runner else 0
        email = f"loadtest_{id(self)}@example.com"

        # Register (ignore failure if the user already exists)
        self.client.post(
            "/register",
            json={"name": "Load Test", "email": email, "password": "password123"},
            name="/register",
        )

        # Login to get a token
        response = self.client.post(
            "/auth/login",
            json={"email": email, "password": "password123"},
            name="/auth/login",
        )

        self.token = None
        if response.status_code == 200:
            self.token = response.json().get("token")

    @task
    def user_journey(self):
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}

        # 1. GET all products
        self.client.get("/products", name="/products")

        # 2. GET a single product by ID
        self.client.get("/products/1", name="/products/<id>")

        # 3. POST a new order (protected -> needs token)
        order_response = self.client.post(
            "/orders",
            json={
                "user_id": 1,
                "total_prices": 10000,
                "products": [
                    {"product_id": 1, "quantity": 1, "product_price": 10000}
                ],
            },
            headers=headers,
            name="/orders",
        )

        # 4. GET the created order
        if order_response.status_code == 201:
            order_id = order_response.json().get("order", {}).get("id")
            if order_id:
                self.client.get(f"/orders/{order_id}", name="/orders/<id>")
