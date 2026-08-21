from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(50),
        default='user'
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    orders = db.relationship("Order", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    products = db.relationship("Product", back_populates="category")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


order_items = db.Table(
    "order_items",
    db.Column(
        "order_id",
        db.Integer,
        db.ForeignKey("orders.id", ondelete="CASCADE"),
        primary_key=True
    ),
    db.Column(
        "product_id",
        db.Integer,
        db.ForeignKey("products.id"),
        primary_key=True
    ),
    db.Column(
        "quantity",
        db.Integer,
        nullable=False
    ),
    db.Column(
        "product_price",
        db.Numeric(12, 2)
    )
)


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)

    categories_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id")
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Numeric(12, 2)
    )

    description = db.Column(
        db.Text
    )

    stock = db.Column(
        db.Integer,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    category = db.relationship("Category", back_populates="products")

    orders = db.relationship(
        "Order",
        secondary=order_items,
        back_populates="products"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "categories_id": self.categories_id,
            "name": self.name,
            "price": float(self.price) if self.price else None,
            "description": self.description,
            "stock": self.stock,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )

    total_prices = db.Column(
        db.Numeric(12, 2)
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now()
    )

    user = db.relationship("User", back_populates="orders")

    products = db.relationship(
        "Product",
        secondary=order_items,
        back_populates="orders"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "total_prices": float(self.total_prices) if self.total_prices else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
