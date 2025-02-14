from flask import Blueprint, request
from services.consumer_service import (
    get_all_consumers, 
    get_consumer_by_id, 
    update_consumer, 
    delete_consumer
)
consumer_bp = Blueprint('consumer', __name__)


# Get All Consumers
@consumer_bp.route('/all', methods=['GET'])
def get_all():
    return get_all_consumers()

# Get Consumer by ID
@consumer_bp.route('/<consumer_id>', methods=['GET'])
def get_by_id(consumer_id):
    return get_consumer_by_id(consumer_id)

# Update Consumer
@consumer_bp.route('/update/<consumer_id>', methods=['PUT'])
def update(consumer_id):
    data = request.json
    return update_consumer(consumer_id, data)

# Delete Consumer
@consumer_bp.route('/delete/<consumer_id>', methods=['DELETE'])
def delete(consumer_id):
    return delete_consumer(consumer_id)