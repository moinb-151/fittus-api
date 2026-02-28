from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from ..models import User


def verify_google_token(token):
    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        return id_info
    
    except Exception as e:
        print(f"Google token verification failed: {e}")
        return None

def get_or_create_google_user(data):
    google_id = data.get('sub')
    email = data.get('email')
    name = data.get('name', '')
    first_name, last_name = (name.split(' ', 1) + [""])[:2] 

    user = User.objects.filter(email=email).first()

    if user:
        if not user.google_id:
            user.google_id = google_id
            user.auth_provider = User.AUTH_PROVIDER_GOOGLE
            user.save()

        return user
    
    user = User.objects.create(
        email=email,
        first_name=first_name,
        last_name=last_name,
        auth_provider=User.AUTH_PROVIDER_GOOGLE,
        google_id=google_id
    )

    return user

def generate_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }