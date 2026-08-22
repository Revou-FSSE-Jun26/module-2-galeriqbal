from functools import wraps
from flask import request, jsonify
import jwt
import os
from models import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Cek header Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # Format: "Bearer <token>"
            parts = auth_header.split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Decode token pakai secret key
            data = jwt.decode(
                token,
                os.getenv('JWT_SECRET_KEY'),
                algorithms=["HS256"]
            )
            # Ambil user dari database berdasarkan user_id di token
            current_user = User.query.get(data['user_id'])
            if current_user is None:
                return jsonify({"error": "User not found"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token is invalid"}), 401

        # Pass current_user ke route function
        return f(current_user, *args, **kwargs)

    return decorated
