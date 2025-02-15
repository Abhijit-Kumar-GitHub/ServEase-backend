from flask import Blueprint, request, jsonify
import uuid
from datetime import datetime
from firebase_admin import firestore
from services.image_service import upload_image

# Hardcoded list of request categories
VALID_CATEGORIES = [
    "Plumbing", "Electrician", "Carpenter", "Painter", "Mechanic",
    "Gardener", "Cleaner", "IT Support"
]

def create_request(data, file=None):
    try:
        db = firestore.client()
        request_id = str(uuid.uuid4())
        # Handle image upload if file is provided
        image_url = None
        if file:
            image_url = upload_image(file)
        # Build request data
        request_data = {
            'id': request_id,
            'consumer_id': data['consumer_id'],
            'service_provider_id': None,
            'title': data['title'],
            'description': data['description'],
            'category': data['category'],
            'image_url': image_url if image_url else '',
            'status': 'open',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        # Debugging: Log received category
        print(f"Received category: {request_data['category']}")
        # Validate category (case-insensitive)
        if request_data['category'].strip().lower() not in [c.lower() for c in VALID_CATEGORIES]:
            return jsonify({"success": False, "message": "Invalid category"}), 400
        # Save request to Firestore
        db.collection('requests').document(request_id).set(request_data)
        return jsonify({"success": True, "message": "Request created successfully", "data": request_data}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# View Open Requests by Category (for Service Providers)
def view_open_requests(category):
    try:
        db = firestore.client()
        if category not in VALID_CATEGORIES:
            return jsonify({"success": False, "message": "Invalid category"}), 400
        
        requests_ref = db.collection('requests').where('category', '==', category).where('status', '==', 'open')
        docs = requests_ref.stream()
        open_requests = [doc.to_dict() for doc in docs]
        
        return jsonify(open_requests), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Accept a Request (for Service Providers)
def accept_request(request_id, service_provider_id):
    try:
        db = firestore.client()
        request_ref = db.collection('requests').document(request_id)
        doc = request_ref.get()

        if doc.exists:
            request_data = doc.to_dict()
            
            if request_data['status'] != 'open':
                return jsonify({"success": False, "message": "Request is not open"}), 400

            request_ref.update({
                'service_provider_id': service_provider_id,
                'status': 'accepted',
                'updated_at': datetime.now()
            })
            return jsonify({"success": True, "message": "Request accepted successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Request not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Get All Requests
def get_all_requests():
    try:
        db = firestore.client()
        requests_ref = db.collection('requests')
        docs = requests_ref.stream()
        requests = [doc.to_dict() for doc in docs]
        return jsonify(requests), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Get Request by ID
def get_request_by_id(request_id):
    try:
        db = firestore.client()
        request_ref = db.collection('requests').document(request_id)
        doc = request_ref.get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"success": False, "message": "Request not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Update Request
def update_request(request_id, data):
    try:
        db = firestore.client()
        request_ref = db.collection('requests').document(request_id)
        doc = request_ref.get()
        if doc.exists:
            update_data = {}
            if 'service_provider_id' in data:
                update_data['service_provider_id'] = data['service_provider_id']
            if 'status' in data:
                update_data['status'] = data['status']
            if 'title' in data:
                update_data['title'] = data['description']
            if 'description' in data:
                update_data['description'] = data['description']
            if 'image_url' in data:
                update_data['image_url'] = data['image_url']
            if 'category' in data and data['category'] in VALID_CATEGORIES:
                update_data['category'] = data['category']
            update_data['updated_at'] = datetime.now()
            request_ref.update(update_data)
            return jsonify({"success": True, "message": "Request updated successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Request not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e), "request_data": update_data }), 500


# Delete Request
def delete_request(request_id):
    try:
        db = firestore.client()
        request_ref = db.collection('requests').document(request_id)
        doc = request_ref.get()
        if doc.exists:
            request_ref.delete()
            return jsonify({"success": True, "message": "Request deleted successfully"}), 200
        else:
            return jsonify({"success": False, "message": "Request not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
