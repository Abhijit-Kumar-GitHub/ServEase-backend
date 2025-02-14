from flask import Blueprint, request, jsonify
from services.otp_service import (
    send_otp_email_with_usertype,
    verify_otp_with_usertype
)

otp_bp = Blueprint('otp', __name__)

@otp_bp.route('/send-otp', methods=['POST'])
def send_otp():
    """Send an OTP to the specified email if the user exists and is not verified."""
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"success": False, "message": "Email is required."}), 400

    success, message = send_otp_email_with_usertype(email)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code

@otp_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verify the OTP and update the verified status based on the user type."""
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    if not email or not otp:
        return jsonify({"success": False, "message": "Email and OTP are required."}), 400

    success, message = verify_otp_with_usertype(email, otp)
    status_code = 200 if success else 400
    return jsonify({"success": success, "message": message}), status_code
