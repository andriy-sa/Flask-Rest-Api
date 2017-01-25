from flask import jsonify
from functools import wraps
from flask_login import current_user


def login_required(is_admin=False):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'message': 'Unauthorized HTTP responses'}), 401

            if is_admin and not current_user.is_admin:
                return jsonify({'message': 'Permission Denied'}), 403

            return func(*args, **kwargs)

        return decorated_view

    return decorator
