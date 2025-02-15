import os
import base64
from flask import Flask
import firebase_admin
from firebase_admin import credentials, firestore
from config import Config
from routes.consumer_routes import consumer_bp
from routes.service_provider_routes import service_provider_bp
from routes.image_routes import image_bp  # Import the image route
from routes.auth_routes import auth_bp
from routes.otp_routes import otp_bp
from routes.offer_routes import offer_bp
from routes.request_routes import request_bp
from routes.rate_review_routes import review_bp
from routes.chatbot_routes import chatbot_bp, init_chatbot_routes # Import the chatbot routes and the initialization function
from services.chatbot_service import GeminiService 


app = Flask(__name__)
app.config.from_object(Config)  


# Decode the environment variable and create the credentials file --->> add it in try catch block later
firebase_credentials_path = "firebase-cred.json"
encoded_credentials = os.environ.get("FIREBASE_CREDENTIALS_BASE64")

if encoded_credentials:
    with open(firebase_credentials_path, "wb") as f:
        f.write(base64.b64decode(encoded_credentials))
# Initialize Firebase with the recreated credentials file
cred = credentials.Certificate(firebase_credentials_path)

try: 
   
    if not firebase_admin._apps:  # Ensure Firebase is initialized only once
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("Firebase initialized successfully")
except Exception as e: 
    print(f"Error initializing Firebase: {str(e)}")    
    db = None

# Register consumer routes
app.register_blueprint(consumer_bp, url_prefix='/consumer')
# Register consumer service- providers routes
app.register_blueprint(service_provider_bp, url_prefix='/service_provider')
# Register consumer request routes
app.register_blueprint(request_bp, url_prefix='/request')
# Register consumer sending offer routes
app.register_blueprint(offer_bp, url_prefix='/offer')
# Register image routes
app.register_blueprint(image_bp, url_prefix='/image')

app.register_blueprint(auth_bp, url_prefix='/auth')

app.register_blueprint(otp_bp, url_prefix='/otp')



app.register_blueprint(review_bp, url_prefix='/rate-review')

# Initialize the Gemini service *once* here
gemini_service = GeminiService()

# Initialize and register the chatbot routes, passing in the Gemini service
app.register_blueprint(init_chatbot_routes(gemini_service), url_prefix='/chatbot')

if __name__ == '__main__':
    app.run(debug=True)