import requests
from datetime import datetime, timedelta
import random, string, os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from firebase_admin import firestore
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()
# Configuration constants
OTP_EXPIRATION_MINUTES = 40  # OTP is valid for 40 minutes
BREVO_API_KEY = os.getenv('BREVO_API_KEY') 
FROM_EMAIL = os.getenv('FROM_EMAIL') 
# Use environment variable for API key

def generate_otp(length=6):
    """Generate a random alphanumeric OTP."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

from datetime import datetime, timedelta, timezone

def store_otp(email, otp):
    """Store the generated OTP in Firestore with an expiration time."""
    db = firestore.client()
    now = datetime.now(timezone.utc)  # Ensure timezone-aware datetime
    otp_data = {
        "otp": otp,
        "created_at": now,
        "expires_at": now + timedelta(minutes=OTP_EXPIRATION_MINUTES)
    }
    db.collection('otps').document(email).set(otp_data)
    print(f"OTP stored for {email}")

def verify_otp(email, otp):
    """Verify if the OTP is valid and not expired."""
    db = firestore.client()
    otp_doc = db.collection('otps').document(email).get()

    if not otp_doc.exists:
        return False, "OTP not found."

    otp_data = otp_doc.to_dict()
    expires_at = otp_data['expires_at']

    # Convert expires_at to a timezone-aware datetime if it isn't already
    if not isinstance(expires_at, datetime):
        return False, "Invalid expiration date."

    expiration_time = expires_at if expires_at.tzinfo else expires_at.replace(tzinfo=timezone.utc)

    if otp_data['otp'] != otp:
        return False, "Invalid OTP."

    if datetime.now(timezone.utc) > expiration_time:
        return False, "OTP has expired."

    # OTP is valid, delete it after verification
    db.collection('otps').document(email).delete()
    return True, "OTP verified successfully."


def send_otp_email(email, otp):
    """Send an OTP email using Brevo (Sendinblue) via HTTP request."""
    url = "https://api.brevo.com/v3/smtp/email"
    payload = {
        "sender": {"email": FROM_EMAIL},  # FROM_EMAIL should be set in your .env
        "to": [{"email": email}],
        "subject": "Your Verification OTP",
        "htmlContent": f"""
            <p>Your OTP is: <strong>{otp}</strong></p>
            <p>This OTP is valid for {OTP_EXPIRATION_MINUTES} minutes.</p>
        """
    }
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        print(f"OTP email sent successfully to {email}. Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to send OTP email: {e}")
        return False


def send_otp_email_with_usertype(email):
    """Send OTP based on the user type (0 for consumer, 1 for service provider)."""
    try:
        db = firestore.client()
        user_docs = db.collection('consumers').where('email', '==', email).get()
        
        if user_docs:
            collection = 'consumers'
            user_data = user_docs[0].to_dict()
        else:
            user_docs = db.collection('service_providers').where('email', '==', email).get()
            if user_docs:
                collection = 'service_providers'
                user_data = user_docs[0].to_dict()
            else:
                return False, "User not found."

        if user_data.get('verified'):
            return False, "User is already verified."

        otp = generate_otp()
        store_otp(email, otp)
        send_otp_email(email, otp)
        return True, f"OTP sent successfully to {email} for {collection}."

    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False, str(e)


def verify_otp_with_usertype(email, otp):
    """Verify the OTP and update the verified status based on the user type (0 for consumer, 1 for service provider)."""
    try:
        db = firestore.client()
        user_docs = db.collection('consumers').where('email', '==', email).get()

        if user_docs:
            collection = 'consumers'
            user_doc_id = user_docs[0].id
        else:
            user_docs = db.collection('service_providers').where('email', '==', email).get()
            if user_docs:
                collection = 'service_providers'
                user_doc_id = user_docs[0].id
            else:
                return False, "User not found."

        is_valid, message = verify_otp(email, otp)
        if is_valid:
            db.collection(collection).document(user_doc_id).update({"verified": True})
            return True, "OTP verified successfully. User is now verified."
        else:
            return False, message

    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return False, str(e)
