
from flask import Blueprint, request
from services.service_provider_service import (
    get_all_service_providers,
    get_service_provider_by_id,
    update_service_provider,
    delete_service_provider
)
service_provider_bp = Blueprint('service_provider', __name__)


# Get All Service Providers
@service_provider_bp.route('/all', methods=['GET'])
def get_all():
    return get_all_service_providers()

# Get Service Provider by ID
@service_provider_bp.route('/<provider_id>', methods=['GET'])
def get_by_id(provider_id):
    return get_service_provider_by_id(provider_id)

# Update Service Provider
@service_provider_bp.route('/update/<provider_id>', methods=['PUT'])
def update(provider_id):
    data = request.get_json()
    return update_service_provider(provider_id, data)

# Delete Service Provider
@service_provider_bp.route('/delete/<provider_id>', methods=['DELETE'])
def delete(provider_id):
    return delete_service_provider(provider_id)