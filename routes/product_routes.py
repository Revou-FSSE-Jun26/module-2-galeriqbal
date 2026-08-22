from flask import Blueprint, jsonify, request
from models import db, Product, order_items
from utils.decorators import token_required

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())

@product_bp.route('/products', methods=['POST'])
@token_required
def create_product(current_user):
    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    if not data.get('name'):
        return jsonify({"error": "name is required"}), 400
    if data.get('price') is None:
        return jsonify({"error": "price is required"}), 400
    if data.get('stock') is None:
        return jsonify({"error": "stock is required"}), 400
    if data['price'] < 0:
        return jsonify({"error": "price must be a positive number"}), 400
    if data['stock'] < 0:
        return jsonify({"error": "stock must be a positive number"}), 400

    new_product = Product(
        categories_id=data.get('categories_id'),
        name=data['name'],
        price=data['price'],
        description=data.get('description'),
        stock=data['stock']
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify(new_product.to_dict()), 201

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_required
def update_product(current_user, product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    data = request.get_json()

    # Validation
    if not data:
        return jsonify({"error": "Request body is required"}), 400
    if 'name' in data and not data['name']:
        return jsonify({"error": "name cannot be empty"}), 400
    if 'price' in data and data['price'] < 0:
        return jsonify({"error": "price must be a positive number"}), 400
    if 'stock' in data and data['stock'] < 0:
        return jsonify({"error": "stock must be a positive number"}), 400

    if 'name' in data:
        product.name = data['name']
    if 'price' in data:
        product.price = data['price']
    if 'description' in data:
        product.description = data['description']
    if 'stock' in data:
        product.stock = data['stock']
    if 'categories_id' in data:
        product.categories_id = data['categories_id']

    db.session.commit()

    return jsonify(product.to_dict())

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
def delete_product(current_user, product_id):
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    # Check if product has active orders
    active_orders = db.session.execute(
        order_items.select().where(order_items.c.product_id == product_id)
    ).fetchall()

    if active_orders:
        return jsonify({"error": "Cannot delete product with active orders"}), 400

    db.session.delete(product)
    db.session.commit()

    return jsonify({"message": "Product deleted successfully"})
