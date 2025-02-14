from flask import Blueprint, request, jsonify
from services.image_service import upload_image

image_bp = Blueprint('image_bp', __name__)


@image_bp.route('/upload', methods=['POST'])
def upload_image_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    
    response = upload_image(image)  # response is now a dictionary
    
    if response.get('url'):
        return jsonify({'url': response['url']}), 200
    else:
        return jsonify({'error': response.get('error', 'Image upload failed')}), 500


# ----------------------------------xoxo------------------------------------