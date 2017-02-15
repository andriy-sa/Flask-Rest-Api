from flask import Blueprint, request, jsonify, current_app, _request_ctx_stack
from flask_login import logout_user, current_user
from app import jwt
from flask_jwt import JWTError
from jwt import InvalidTokenError

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get(current_app.config.get('JWT_AUTH_USERNAME_KEY'), None)
    password = data.get(current_app.config.get('JWT_AUTH_PASSWORD_KEY'), None)
    criterion = [username, password, len(data) == 2]

    if not all(criterion):
        raise JWTError('Bad Request', 'Invalid credentials')

    user = jwt.authentication_callback(username, password)
    if user:
        access_token = jwt.jwt_encode_callback(user)

        return jsonify({'user': user.serialize(), 'access_token': access_token.decode('utf-8')}), 200
    else:
        raise JWTError('Bad Request', 'Invalid credentials')



@auth_view.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify({'status': 'success'}), 200


@auth_view.route('/me', methods=['GET'])
def me():
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

    return jsonify(identity), 200
