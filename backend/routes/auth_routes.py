from flask import Blueprint, request, jsonify
from services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register/<user_type>', methods=['POST'])
def register(user_type):
    """Register a new consumer or service provider."""
    try:
        data = request.get_json()
        
        user_data = register_user(data, user_type)
        return jsonify({"success": True, "message": "User registered successfully", "user_data": user_data}), 201

    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@auth_bp.route('/login/<user_type>', methods=['POST'])
def login(user_type):
    """Login a consumer or service provider."""
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400
        
        user_data = login_user(email, password, user_type)
        return jsonify({"success": True, "message": "Login successful", "user_data": user_data}), 200

    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
