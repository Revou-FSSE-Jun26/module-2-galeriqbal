from flask import Blueprint, jsonify, request
from models import db, Order, Product, order_items
from utils.decorators import token_required

order_bp = Blueprint('orders', __name__)

@order_bp.route('/orders', methods=['GET'])
def get_orders():
    limit = request.args.get('limit', default=50, type=int)
    query = Order.query

    # Filter opsional: order milik satu user (customer lihat order sendiri)
    user_id = request.args.get('user_id', type=int)
    if user_id:
        query = query.filter(Order.user_id == user_id)

    orders = query.order_by(Order.id.desc()).limit(limit).all()
    return jsonify([order.to_dict() for order in orders])

@order_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    # Include order items in response
    items = db.session.execute(
        order_items.select().where(order_items.c.order_id == order_id)
    ).fetchall()

    result = order.to_dict()
    result["products"] = []
    for item in items:
        product = Product.query.get(item.product_id)
        result["products"].append({
            "product_id": item.product_id,
            "product_name": product.name if product else None,
            "quantity": item.quantity,
            "product_price": float(item.product_price) if item.product_price else None
        })

    return jsonify(result)

@order_bp.route('/orders', methods=['POST'])
@token_required
def create_order(current_user):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400
    if not data.get('user_id'):
        return jsonify({"error": "user_id is required"}), 400
    if not data.get('products'):
        return jsonify({"error": "products list is required"}), 400

    # Create order
    order = Order(
        user_id=data['user_id'],
        total_prices=data.get('total_prices', 0)
    )
    db.session.add(order)
    db.session.flush()

    # Link products via order_items
    for item in data['products']:
        db.session.execute(order_items.insert().values(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            product_price=item.get('product_price', 0)
        ))

    db.session.commit()

    return jsonify({
        "message": "Order created successfully",
        "order": order.to_dict(),
        "products_linked": [item['product_id'] for item in data['products']]
    }), 201

@order_bp.route('/orders/<int:order_id>', methods=['PUT'])
@token_required
def update_order(current_user, order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body is required"}), 400

    if 'user_id' in data:
        order.user_id = data['user_id']
    if 'total_prices' in data:
        order.total_prices = data['total_prices']

    db.session.commit()

    return jsonify(order.to_dict())

@order_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@token_required
def delete_order(current_user, order_id):
    order = Order.query.get(order_id)
    if order is None:
        return jsonify({"error": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({"message": "Order deleted successfully"})
