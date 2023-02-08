from datetime import datetime, timedelta

import jwt
from django.conf import settings

ACCESS_TOKEN_LIFETIME = getattr(settings, 'ACCESS_TOKEN_LIFETIME', 3600)
REFRESH_TOKEN_LIFETIME = getattr(settings, 'REFRESH_TOKEN_LIFETIME', 3600*12)


def generate_access_token(user):
    now = datetime.now()
    issued_at = int(now.timestamp())
    expires_at = int((now + timedelta(seconds=ACCESS_TOKEN_LIFETIME)).timestamp())
    access_token = jwt.encode(
        {'user_id': user.id,
         'token_type': 'access',
         'issued_at': issued_at,
         'expires_at': expires_at},
        settings.SECRET_KEY,
        algorithm='HS512'
    )
    return access_token


def generate_refresh_token(user):
    user
    now = datetime.now()
    issued_at = int(now.timestamp())
    expires_at = int((now + timedelta(seconds=REFRESH_TOKEN_LIFETIME)).timestamp())
    refresh_token = jwt.encode(
        {'user_id': user.id,
         'token_type': 'refresh',
         'token_count': user.refresh_token_count + 1, 
         'issued_at': issued_at,
         'expires_at': expires_at},
        settings.SECRET_KEY,
        algorithm='HS512'
    )
    return refresh_token


def decode_token(token):
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=['HS512']
    )
    return payload


def verify_token(token):
    try:
        payload = decode_token(token)
    except jwt.exceptions.DecodeError:
        return False, None

    now = datetime.utcnow()
    expires_at = payload.get('expires_at')

    if not expires_at or now > datetime.fromtimestamp(expires_at):
        return False, None

    return True, payload['user_id']
