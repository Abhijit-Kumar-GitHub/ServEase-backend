from flask import Blueprint, request
from services.rate_review_service import (
    create_review, get_all_reviews, get_reviews_by_provider, get_reviews_by_consumer, 
    update_review, delete_review
)

review_bp = Blueprint('rate-review', __name__)

#  Create a review (Ensures consumer_id & service_provider_id exist)
@review_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return create_review(data)

#  Get all reviews
@review_bp.route('/all', methods=['GET'])
def get_all():
    return get_all_reviews()

#  Get reviews for a specific service provider
@review_bp.route('/provider/<string:service_provider_id>', methods=['GET'])
def get_by_provider(service_provider_id):
    return get_reviews_by_provider(service_provider_id)

#  Get all reviews filed by a specific consumer
@review_bp.route('/consumer/<string:consumer_id>', methods=['GET'])
def get_by_consumer(consumer_id):
    return get_reviews_by_consumer(consumer_id)

#  Update a review (Validates input)
@review_bp.route('/update/<string:review_id>', methods=['PUT'])
def update(review_id):
    data = request.get_json()
    return update_review(review_id, data)

#  Delete a review
@review_bp.route('/delete/<string:review_id>', methods=['DELETE'])
def delete(review_id):
    return delete_review(review_id)
