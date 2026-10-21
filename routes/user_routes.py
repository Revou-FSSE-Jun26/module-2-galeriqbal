from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash
import jwt
import os
from datetime import datetime, timedelta, timezone
from models import db, User

user_bp = Blueprint('users', __name__)

ALLOWED_ROLES = ("customer", "admin")

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "name, email, and password are required"}), 400

    # Email harus unik
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409

    # Role: default customer. Hanya boleh customer / admin.
    role = data.get('role', 'customer')
    if role not in ALLOWED_ROLES:
        return jsonify({"error": "role must be 'customer' or 'admin'"}), 400

    new_user = User(
        name=data['name'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=role
    )

    db.session.add(new_user)
    db.session.commit()

    # Auto-login: langsung kasih token setelah register.
    token = jwt.encode(
        {
            "user_id": new_user.id,
            "email": new_user.email,
            "role": new_user.role,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        os.getenv('JWT_SECRET_KEY'),
        algorithm="HS256"
    )

    return jsonify({
        "message": "User registered successfully",
        "token": token,
        "user": new_user.to_dict()
    }), 201

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict())
