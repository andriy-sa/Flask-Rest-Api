from flask import jsonify, _request_ctx_stack
from functools import wraps
from flask_jwt import JWTError
from jwt import InvalidTokenError
from app import jwt


def login_required(is_admin=False):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            token = jwt.request_callback()

            if token is None:
                raise JWTError('Authorization Required', 'Request does not contain an access token',
                               headers={'WWW-Authenticate': 'JWT realm="%s"' % 'token'})

            try:
                payload = jwt.jwt_decode_callback(token)
            except InvalidTokenError as e:
                raise JWTError('Invalid token', str(e))

            _request_ctx_stack.top.current_identity = identity = jwt.identity_callback(payload)

            if identity is None:
                raise JWTError('Invalid JWT', 'User does not exist')

            if is_admin and not identity['is_admin']:
                return jsonify({'message': 'Permission Denied'}), 403

            return func(*args, **kwargs)

        return decorated_view

    return decorator
