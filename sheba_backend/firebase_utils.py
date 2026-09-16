import os
import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # Assuming firebase-service-account.json is in the project root
            cred_path = os.path.join(settings.BASE_DIR, 'firebase-service-account.json')
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase Admin SDK initialized successfully.")
            else:
                logger.warning(f"Firebase credentials not found at {cred_path}. Push notifications will not work.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")

def send_push_notification(user, title, body, data=None):
    if not user.fcm_token:
        logger.info(f"User {user.email} does not have an FCM token.")
        return False
        
    if not firebase_admin._apps:
        logger.warning("Firebase Admin SDK is not initialized. Cannot send notification.")
        return False

    if data is None:
        data = {}

    # Ensure all data values are strings
    stringified_data = {str(k): str(v) for k, v in data.items()}

    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=stringified_data,
            token=user.fcm_token,
        )
        response = messaging.send(message)
        logger.info(f"Successfully sent message to {user.email}: {response}")
        return True
    except Exception as e:
        logger.error(f"Error sending message to {user.email}: {str(e)}")
        return False
