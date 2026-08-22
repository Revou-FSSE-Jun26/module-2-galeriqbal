from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
from models import db, User

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "name, email, and password are required"}), 400

    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password'])
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": new_user.to_dict()
    }), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())
