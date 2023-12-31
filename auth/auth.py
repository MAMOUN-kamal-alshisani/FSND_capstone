import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os
import requests
from dotenv import load_dotenv
load_dotenv()
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')

## AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    authorization = request.headers.get('authorization')
    if authorization is None:   
        raise AuthError({'code': 'no authorization header',
                'description': 'no authorization header found!'},401)
    if authorization.split()[0] != 'Bearer':   
        raise AuthError({'code': 'bearer type authorization header not found',
                'description': 'authorization header should be of type (Bearer)!'},401)


    token = authorization.split()[1]
    
    if len(token) <= 0:
        raise AuthError('no token has been found!',401)

    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Requested Permission not found.'
        }, 401)

    return True

def verify_decode_jwt(token):
    # jsonurl = requests.get('https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    # jwks = jsonurl.json()
    unverified_Header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_Header:
        raise AuthError({
            'code': 'invalid_authorization_header',
            'description': 'Authorization Header is malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_Header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/',
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                    'Incorrect claims. Please check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_authorization_header',
                'description': 'Unable to parse authentication token.'
            }, 401)

    raise AuthError({
        'code': 'invalid_authorization_header',
        'description': 'Unable to find the appropriate key.'
    }, 401)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator