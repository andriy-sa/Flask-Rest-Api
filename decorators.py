from flask import jsonify, _request_ctx_stack, g
from functools import wraps
from flask_jwt import JWTError
from jwt import InvalidTokenError
from app import jwt


def login_required(is_admin=False):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):

            if g.user is None:
                raise JWTError('Invalid JWT', 'User does not exist')

            if is_admin and not g.user['is_admin']:
                return jsonify({'message': 'Permission Denied'}), 403

            return func(*args, **kwargs)

        return decorated_view

    return decorator
