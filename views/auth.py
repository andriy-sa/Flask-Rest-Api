from flask import Blueprint, request, jsonify, current_app, g
from app import jwt, socketio
from flask_socketio import emit
from flask_jwt import JWTError
from helpers import get_jwt_user

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


@auth_view.route('/me', methods=['GET'])
def me():

    if g.user is None:
        raise JWTError('Invalid JWT', 'User does not exist')

    return jsonify(g.user), 200


# Sockets events
@socketio.on('connect')
def test_connect():
    print(request.headers)
    emit('flask', {'data': 'Connected'})


@socketio.on('test_event')
def test_event(message):
    print(message)
    user = get_jwt_user()
    print(user)
    emit('flask', {'data': 'test event received'})
