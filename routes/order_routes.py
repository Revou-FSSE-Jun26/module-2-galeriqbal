from flask import Blueprint, jsonify
from models import db, Order, order_items

order_bp = Blueprint('orders', __name__)

@order_bp.route('/seed-order', methods=['POST'])
def seed_order():
    # Insert sample data: 1 order linked to multiple products (many-to-many)
    order = Order(user_id=1, total_prices=25500)
    db.session.add(order)
    db.session.flush()  # get order.id before inserting into order_items

    # Link this order to 3 products via order_items
    db.session.execute(order_items.insert().values([
        {"order_id": order.id, "product_id": 1, "quantity": 1, "product_price": 10000},
        {"order_id": order.id, "product_id": 6, "quantity": 1, "product_price": 25000},
        {"order_id": order.id, "product_id": 18, "quantity": 1, "product_price": 2400},
    ]))

    db.session.commit()

    return jsonify({
        "message": "Order created with multiple products (many-to-many)",
        "order_id": order.id,
        "products_linked": [1, 6, 18]
    }), 201

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    # Query order_items to show the many-to-many data
    items = db.session.execute(
        order_items.select().where(order_items.c.order_id == order_id)
    ).fetchall()

    return jsonify({
        "order_id": order.id,
        "user_id": order.user_id,
        "total_prices": float(order.total_prices) if order.total_prices else None,
        "products": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "product_price": float(item.product_price) if item.product_price else None
            } for item in items
        ]
    })
