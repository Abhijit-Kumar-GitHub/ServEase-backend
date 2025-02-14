from flask import jsonify
from firebase_admin import firestore


VALID_CATEGORIES = [
    "Plumber", "Electrician", "Carpenter", "Painter", "Mechanic",
    "Gardener", "Cleaner", "IT Support"
]

# Update Service Provider with category validation
def update_service_provider(provider_id, data):
    try:
        db = firestore.client()
        provider_ref = db.collection('service_providers').document(provider_id)
        doc = provider_ref.get()
        if doc.exists:
            update_data = {}

            if 'name' in data:
                update_data['name'] = data['name']
            if 'phone' in data:
                update_data['phone'] = data['phone']
            if 'email' in data:
                update_data['email'] = data['email']
            if 'category' in data:
                if data['category'] not in VALID_CATEGORIES:
                    return jsonify({"success": False, "message": "Invalid category. Please choose a valid category."}), 400
                update_data['category'] = data['category']
            if 'address' in data:
                update_data['address'] = {
                    'apartment_number': data['address'].get('apartment_number'),
                    'building': data['address'].get('building'),
                    'street': data['address'].get('street'),
                    'pin': data['address'].get('pin'),
                    'landmark': data['address'].get('landmark')
                }

            provider_ref.update(update_data)
            return jsonify({"success": True, "message": "Service provider updated successfully."}), 200
        else:
            return jsonify({"success": False, "message": "Service provider not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Get All Service Providers
def get_all_service_providers():
    try:
        db = firestore.client()
        providers_ref = db.collection('service_providers')
        docs = providers_ref.stream()
        providers = [doc.to_dict() for doc in docs]
        return jsonify(providers), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Get Service Provider by ID
def get_service_provider_by_id(provider_id):
    try:
        db = firestore.client()
        provider_ref = db.collection('service_providers').document(provider_id)
        doc = provider_ref.get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"success": False, "message": "Service provider not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Delete Service Provider
def delete_service_provider(provider_id):
    try:
        db = firestore.client()
        provider_ref = db.collection('service_providers').document(provider_id)
        doc = provider_ref.get()
        if doc.exists:
            provider_ref.delete()
            return jsonify({"success": True, "message": "Service provider deleted successfully."}), 200
        else:
            return jsonify({"success": False, "message": "Service provider not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500