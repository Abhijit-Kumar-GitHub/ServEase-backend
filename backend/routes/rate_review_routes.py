from flask import Blueprint, request
from services.rate_review_service import (
    create_review, get_all_reviews, get_reviews_by_provider, update_review, delete_review
)

review_bp = Blueprint('rate-review', __name__)

@review_bp.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    return create_review(data)

@review_bp.route('/all', methods=['GET'])
def get_all():
    return get_all_reviews()

@review_bp.route('/provider/<string:service_provider_id>', methods=['GET'])
def get_by_provider(service_provider_id):
    return get_reviews_by_provider(service_provider_id)

@review_bp.route('/update/<string:review_id>', methods=['PUT'])
def update(review_id):
    data = request.get_json()
    return update_review(review_id, data)

@review_bp.route('/delete/<string:review_id>', methods=['DELETE'])
def delete(review_id):
    return delete_review(review_id)
