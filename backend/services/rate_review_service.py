
from flask import jsonify
import uuid
from datetime import datetime
from firebase_admin import firestore

def create_review(data):
    try:
        db = firestore.client()
        review_id = str(uuid.uuid4())

        # Extract required fields
        consumer_id = data.get('consumer_id')
        service_provider_id = data.get('service_provider_id')
        rating = data.get('rating')
        review_text = data.get('review')
        # request_id=data.get('request_id')

        # Validate user existence
        consumer_ref = db.collection('users').document(consumer_id).get()
        provider_ref = db.collection('service_providers').document(service_provider_id).get()

        if not consumer_ref.exists:
            return jsonify({"success": False, "message": "Invalid consumer ID"}), 400
        
        if not provider_ref.exists:
            return jsonify({"success": False, "message": "Invalid service provider ID"}), 400

        # Validate rating (must be a number from 1 to 10)
        if not isinstance(rating, int) or rating < 1 or rating > 10:
            return jsonify({"success": False, "message": "Rating must be an integer between 1 and 10"}), 400
        
        # Validate review (must be a string)
        if not isinstance(review_text, str) or not review_text.strip():
            return jsonify({"success": False, "message": "Review must be a non-empty string"}), 400

        # Build review data
        review_data = {
            'id': review_id,
            'consumer_id': consumer_id,
            'service_provider_id': service_provider_id,
            'review': review_text.strip(),
            'category': data['category'],
            'rating': rating,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        # Save review to Firestore
        db.collection('rate_review').document(review_id).set(review_data)

        return jsonify({"success": True, "message": "Review created successfully", "data": review_data}), 201

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500



def get_all_reviews():
    try:
        db = firestore.client()
        reviews_ref = db.collection('rate_review')
        docs = reviews_ref.stream()
        reviews = [doc.to_dict() for doc in docs]

        return jsonify({"success": True, "reviews": reviews}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def get_reviews_by_provider(service_provider_id):
    try:
        db = firestore.client()
        reviews_ref = db.collection('rate_review').where('service_provider_id', '==', service_provider_id)
        docs = reviews_ref.stream()
        reviews = [doc.to_dict() for doc in docs]

        return jsonify({"success": True, "reviews": reviews}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def update_review(review_id, data):
    try:
        db = firestore.client()
        review_ref = db.collection('rate_review').document(review_id)
        doc = review_ref.get()

        if not doc.exists:
            return jsonify({"success": False, "message": "Review not found"}), 404

        update_data = {}

        if 'rating' in data:
            rating = data['rating']
            if not isinstance(rating, int) or rating < 1 or rating > 10:
                return jsonify({"success": False, "message": "Rating must be an integer between 1 and 10"}), 400
            update_data['rating'] = rating

        if 'review' in data:
            review_text = data['review']
            if not isinstance(review_text, str) or not review_text.strip():
                return jsonify({"success": False, "message": "Review must be a non-empty string"}), 400
            update_data['review'] = review_text.strip()

        update_data['updated_at'] = datetime.now()

        review_ref.update(update_data)

        return jsonify({"success": True, "message": "Review updated successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


def delete_review(review_id):
    try:
        db = firestore.client()
        review_ref = db.collection('rate_review').document(review_id)
        doc = review_ref.get()

        if not doc.exists:
            return jsonify({"success": False, "message": "Review not found"}), 404

        review_ref.delete()

        return jsonify({"success": True, "message": "Review deleted successfully"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

def get_reviews_by_consumer(consumer_id):
    """Fetch all reviews filed by a specific consumer."""
    try:
        db = firestore.client()
        reviews_ref = db.collection('rate_review').where('consumer_id', '==', consumer_id)
        docs = reviews_ref.stream()
        reviews = [doc.to_dict() for doc in docs]

        return jsonify({"success": True, "reviews": reviews}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
