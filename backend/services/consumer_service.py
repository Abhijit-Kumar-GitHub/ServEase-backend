from flask import jsonify
from firebase_admin import firestore




# Get All Consumers
def get_all_consumers():
    try:
        db = firestore.client()

        consumers_ref = db.collection('consumers')
        docs = consumers_ref.stream()
        consumers = [doc.to_dict() for doc in docs]
        return jsonify(consumers), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Get Consumer by ID
def get_consumer_by_id(consumer_id):
    try:
        db = firestore.client()

        consumer_ref = db.collection('consumers').document(consumer_id)
        doc = consumer_ref.get()
        if doc.exists:
            return jsonify(doc.to_dict()), 200
        else:
            return jsonify({"success": False, "message": "Consumer not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# Update Consumer
def update_consumer(consumer_id, data):
    try:
        db = firestore.client()

        consumer_ref = db.collection('consumers').document(consumer_id)
        doc = consumer_ref.get()
        if doc.exists:
            update_data = {}

            if 'name' in data:
                update_data['name'] = data['name']
            if 'phone' in data:
                update_data['phone'] = data['phone']
            if 'email' in data:
                update_data['email'] = data['email']
            if 'aadhaar' in data:
                update_data['aadhaar'] = data['aadhaar']
            if 'address' in data:
                update_data['address'] = {
                    'apartment_number': data['address'].get('apartment_number'),
                    'building': data['address'].get('building'),
                    'street': data['address'].get('street'),
                    'pin': data['address'].get('pin'),
                    'landmark': data['address'].get('landmark')
                }

            consumer_ref.update(update_data)
            return jsonify({"success": True, "message": "Consumer updated successfully."}), 200
        else:
            return jsonify({"success": False, "message": "Consumer not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)+"hemloooo"}), 500

# """
# dummy json for update  
# {
#   "name": "Jane Doe",
#   "phone": "9876543210",
#   "email": "janedoe@example.com",
#   "aadhaar": "9012-3456-7890",
#   "address": {
#     "apartment_number": "202",
#     "building": "Skyline Towers",
#     "street": "Broadway Street",
#     "pin": "560002",
#     "landmark": "Near Central Mall"
#   }
# }

# dummy json for partial-update
# {
#   "email": "updatedemail@example.com",
#   "phone": "1122334455"
# }
# """

# Delete Consumer
def delete_consumer(consumer_id):
    try:
        db = firestore.client()

        consumer_ref = db.collection('consumers').document(consumer_id)
        doc = consumer_ref.get()
        if doc.exists:
            consumer_ref.delete()
            return jsonify({"success": True, "message": "Consumer deleted successfully."}), 200
        else:
            return jsonify({"success": False, "message": "Consumer not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500