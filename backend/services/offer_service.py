from datetime import datetime
from firebase_admin import firestore
import uuid

def create_offer_service(request_id, data):
    """Service for creating an offer."""
    db = firestore.client()
    offer_id = str(uuid.uuid4())

    if not data.get('service_provider_id') or not data.get('price'):
        raise ValueError("Service provider ID and price are required")

    offer_data = {
        'offer_id': offer_id,
        'service_provider_id': data['service_provider_id'],
        'price': data['price'],
        'message': data.get('message', ''),
        'status': 'pending',
        'created_at': datetime.now()
    }
    

    db.collection('requests').document(request_id).collection('offers').document(offer_id).set(offer_data)
    return offer_id




def get_offers_service(request_id):
    """Service for retrieving all offers for a specific request."""
    db = firestore.client()
    offers_ref = db.collection('requests').document(request_id).collection('offers')
    return [offer.to_dict() for offer in offers_ref.stream()]


def respond_to_offer_service(request_id, offer_id, status):
    """Service for updating the status of an offer."""
    db = firestore.client()

    if status not in ['accepted', 'declined']:
        raise ValueError("Invalid status. Must be 'accepted' or 'declined'")

    db.collection('requests').document(request_id).collection('offers').document(offer_id).update({
        'status': status,
        'updated_at': datetime.now()
    })