from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash
import jwt
import os
from datetime import datetime, timedelta, timezone
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user is None or not check_password_hash(user.password_hash, data['password']):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        },
        os.getenv('JWT_SECRET_KEY'),
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": user.to_dict()
    })
