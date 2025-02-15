from flask import Blueprint, request, jsonify
from services.offer_service import create_offer_service, get_offers_service, respond_to_offer_service
offer_bp = Blueprint('offer_bp', __name__)

@offer_bp.route("/requests/<string:request_id>/offers/create", methods=["POST"])
def create_offer(request_id):
    try:
        if not request.is_json:
            return jsonify({"success": False, "message": "Invalid JSON format"}), 400

        data = request.get_json()  # 🔹 FIX: Ensure we get a dictionary

        offer_id = create_offer_service(request_id, data)
        return jsonify({"success": True, "message": "Offer created successfully", "offer_data": data}), 201

    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@offer_bp.route('/all/<request_id>', methods=['GET'])
def get_offers(request_id):
    """User retrieves all offers for a specific request."""
    try:
        offers = get_offers_service(request_id)
        return jsonify({"success": True, "offers": offers}), 200

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@offer_bp.route('/<request_id>/<offer_id>/respond', methods=['POST'])
def respond_to_offer(request_id, offer_id):
    """User accepts or declines a service provider's offer."""
    try:
        data = request.get_json()
        respond_to_offer_service(request_id, offer_id, data.get('status'))
        message = f"Offer {data.get('status')} successfully"
        return jsonify({"success": True, "message": message}), 200

    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500