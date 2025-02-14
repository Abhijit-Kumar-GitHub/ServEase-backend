from flask import Blueprint, request
from services.request_service import (
    create_request, get_all_requests, get_request_by_id, update_request, delete_request
)

request_bp = Blueprint('request_bp', __name__)

@request_bp.route('/create', methods=['POST'])
def create():
    if request.is_json:
        data = request.get_json()  # Use for JSON data
    else:
        data = request.form.to_dict()  # Use for form data

    file = request.files.get('image')
    
    # Call the create_request function and return its response
    response = create_request(data, file)
    return response  # Assuming create_request already returns a Flask response (jsonify)

# Route to get all requests
@request_bp.route('/all', methods=['GET'])
def get_all():
    return get_all_requests()

# Route to get a request by ID
@request_bp.route('/<string:request_id>', methods=['GET'])
def get_by_id(request_id):
    return get_request_by_id(request_id)

# Route to update a request
@request_bp.route('/update/<string:request_id>', methods=['PUT'])
def update(request_id):
    data = request.get_json()
    return update_request(request_id, data)

# Route to delete a request
@request_bp.route('/delete/<string:request_id>', methods=['DELETE'])
def delete(request_id):
    return delete_request(request_id)