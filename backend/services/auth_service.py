from datetime import datetime, timedelta
from firebase_admin import firestore
import bcrypt
import jwt  # JSON Web Token
import uuid
import os, requests
from flask import jsonify, Blueprint
from dotenv import load_dotenv
load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET', 'your_secret_key')
JWT_EXPIRATION_TIME = int(os.getenv('JWT_EXPIRATION_TIME', 60))  # Token valid for 60 minutes
# Hard-coded list of valid categories. might add other categories later as  needed
VALID_CATEGORIES = [
    "Plumbing", "Electrician", "Carpenter", "Painter", "Mechanic",
    "Gardener", "Cleaner", "IT Support"
]
BREVO_API_KEY = os.getenv('BREVO_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
def send_welcome_email(to_email, user_name):
    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {"email": FROM_EMAIL},
        "to": [{"email": to_email}],
        "subject": "Welcome to Our Service!",
        "htmlContent": f"<h1>Hi {user_name},</h1><p>Welcome to SERVE-EASE!</p>"
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Email sent to {to_email}. Status: {response.status_code}")
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send email: {e}")
        return None, {"error": str(e)}
    
def register_user(data, user_type):
    """
    Register the user and send a welcome email. 
    For consumer, user_type=0
    For service_provider, user_type=1
    Insert your existing registration logic here, hash password, store in Firestore, etc.
    """
    db = firestore.client()
    user_id = str(uuid.uuid4())
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {
        'id': user_id,
        'name': data['name'],
        'phone': data['phone'],
        'email': data['email'],
        'password': hashed_password,
        'verified': False,
        'created_at': datetime.now(),
        'address': data.get('address', {}),
    }
    if user_type == "0":
        db.collection('consumers').document(user_id).set(user_data)
    elif user_type == "1":
        user_data['category'] = data['category']
        db.collection('service_providers').document(user_id).set(user_data)
    del user_data['password']
    # Call send_welcome_email after successful registration
    status, response = send_welcome_email(data['email'], data['name'])
    if status == 200:
        print(f"Successfully sent welcome email to {data['email']}")
    else:
        print(f"Failed to send welcome email. Response: {response}")
    if status != 200:
        print(f"Failed to send welcome email. Response: {response}")
    print("Attempting to send welcome email...")
    return user_data  # Return registered user data


def login_user(email, password):
    """Login and return user data along with a JWT token."""
    db = firestore.client()
    user = None
    user_type = None

    # Check in the 'consumer' collection
    consumer_ref = db.collection("consumers").where('email', '==', email).stream()
    for doc in consumer_ref:
        user = doc.to_dict()
        user_type = "0"
        break

    # If not found in 'consumer', check in 'service_provider'
    if not user:
        service_provider_ref = db.collection("service_providers").where('email', '==', email).stream()
        for doc in service_provider_ref:
            user = doc.to_dict()
            user_type = "1"
            break

    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        raise ValueError("Invalid email or password.")

    # Remove the password from the user data
    del user['password']
    
    # Generate JWT token
    token = jwt.encode(
        {
            "id": user['id'],
            "user_type": user_type,
            "exp": datetime.now() + timedelta(hours=24)
        },
        JWT_SECRET,
        algorithm="HS256"
    )

    return {"user_data": user, "token": token}


    
    
    
def verify_token(token):
    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return decoded
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        raise ValueError("Invalid token")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise ValueError("Token verification failed")
    
    
    