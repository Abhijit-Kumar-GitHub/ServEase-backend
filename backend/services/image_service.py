import cloudinary
import cloudinary.uploader 
import cloudinary.api
import os
from dotenv import load_dotenv
from flask import jsonify
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
) 
def upload_image(image):
    try:
        response = cloudinary.uploader.upload(image)
        return {'url': response.get('secure_url')}
    except Exception as e:
        return {'error': str(e)}
