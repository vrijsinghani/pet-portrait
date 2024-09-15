# firebase.py
import firebase_admin
from firebase_admin import credentials, auth, storage
from django.conf import settings

def initialize_firebase():
  if not firebase_admin._apps:
      cred = credentials.Certificate({
          "type": "service_account",
          "project_id": settings.FIREBASE_PROJECT_ID,
          "client_email": settings.FIREBASE_CLIENT_EMAIL,
          "private_key": settings.FIREBASE_PRIVATE_KEY,
      })
      firebase_admin.initialize_app(cred, {
          'storageBucket': f"{settings.FIREBASE_PROJECT_ID}.appspot.com"
      })

initialize_firebase()