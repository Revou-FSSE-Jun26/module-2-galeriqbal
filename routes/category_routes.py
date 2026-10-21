from flask import Blueprint, jsonify, request
from models import db, Category, Product
from utils.decorators import admin_required

category_bp = Blueprint('categories', __name__)

@category_bp.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])

@category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(category.to_dict())

@category_bp.route('/categories', methods=['POST'])
@admin_required
def create_category(current_user):
    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({"error": "name is required"}), 400

    new_category = Category(name=data['name'])

    db.session.add(new_category)
    db.session.commit()

    return jsonify(new_category.to_dict()), 201

@category_bp.route('/categories/<int:category_id>', methods=['PUT'])
@admin_required
def update_category(current_user, category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    data = request.get_json()

    if not data or not data.get('name'):
        return jsonify({"error": "name is required"}), 400

    category.name = data['name']
    db.session.commit()

    return jsonify(category.to_dict())

@category_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@admin_required
def delete_category(current_user, category_id):
    category = Category.query.get(category_id)
    if category is None:
        return jsonify({"error": "Category not found"}), 404

    # Deletion guard: jangan hapus kategori yang masih punya produk.
    linked = Product.query.filter_by(categories_id=category_id).first()
    if linked:
        return jsonify({"error": "Cannot delete category with linked products"}), 400

    db.session.delete(category)
    db.session.commit()

    return jsonify({"message": "Category deleted successfully"})
