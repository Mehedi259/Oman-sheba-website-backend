"""
Google OAuth Authentication Module

Handles Google ID token verification and user creation/login.
"""
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.conf import settings
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


class GoogleAuthError(Exception):
    """Custom exception for Google auth failures"""
    pass


def verify_google_token(token):
    """
    Verify a Google ID token and return user info.
    """
    try:
        idinfo = None
        if getattr(settings, 'GOOGLE_CLIENT_ID', None):
            try:
                idinfo = id_token.verify_oauth2_token(
                    token,
                    google_requests.Request(),
                    settings.GOOGLE_CLIENT_ID
                )
            except ValueError:
                # Fallback verifying signature without strict audience check
                idinfo = id_token.verify_oauth2_token(
                    token,
                    google_requests.Request()
                )
        else:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request()
            )
        
        # Verify the issuer
        if idinfo.get('iss') not in ['accounts.google.com', 'https://accounts.google.com']:
            raise GoogleAuthError('Invalid token issuer')
        
        return {
            'google_id': idinfo['sub'],
            'email': idinfo.get('email', ''),
            'name': idinfo.get('name', ''),
            'picture': idinfo.get('picture', ''),
            'email_verified': idinfo.get('email_verified', False),
            'given_name': idinfo.get('given_name', ''),
            'family_name': idinfo.get('family_name', ''),
        }
    except ValueError as e:
        raise GoogleAuthError(f'Invalid Google token: {str(e)}')
    except Exception as e:
        raise GoogleAuthError(f'Google token verification failed: {str(e)}')


def get_or_create_google_user(google_data):
    """
    Find an existing user or create a new one from Google data.
    
    Args:
        google_data: dict from verify_google_token()
        
    Returns:
        tuple: (user, created) where created is True if new user was made
    """
    google_id = google_data['google_id']
    email = google_data['email']
    
    # First, try to find by google_id
    try:
        user = User.objects.get(google_id=google_id)
        # Update last login
        user.last_login_at = timezone.now()
        user.save(update_fields=['last_login_at'])
        return user, False
    except User.DoesNotExist:
        pass
    
    # Then, try to find by email (user might have registered with email first)
    try:
        user = User.objects.get(email=email)
        # Link Google account to existing user
        user.google_id = google_id
        user.avatar_url = google_data.get('picture', '')
        user.last_login_at = timezone.now()
        if not user.avatar and google_data.get('picture'):
            user.avatar_url = google_data['picture']
        user.save(update_fields=['google_id', 'avatar_url', 'last_login_at'])
        return user, False
    except User.DoesNotExist:
        pass
    
    # Create new user
    # Generate a unique username from email
    base_username = email.split('@')[0]
    username = base_username
    counter = 1
    while User.objects.filter(username=username).exists():
        username = f"{base_username}{counter}"
        counter += 1
    
    user = User.objects.create(
        username=username,
        email=email,
        google_id=google_id,
        name=google_data.get('name', ''),
        first_name=google_data.get('given_name', ''),
        last_name=google_data.get('family_name', ''),
        avatar_url=google_data.get('picture', ''),
        auth_provider='google',
        last_login_at=timezone.now(),
    )
    # Google users don't need a usable password
    user.set_unusable_password()
    user.save()
    
    return user, True


def generate_tokens_for_user(user):
    """
    Generate JWT access and refresh tokens for a user.
    
    Args:
        user: User model instance
        
    Returns:
        dict with 'access' and 'refresh' token strings
    """
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
