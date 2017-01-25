from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from models.user import User

auth_view = Blueprint('auth_view', __name__)


@auth_view.route('/login', methods=['POST'])
def login():
    form = LoginForm(request.form)
    if not form.validate():
        return jsonify(form.errors), 401

    user = form.user
    login_user(user, remember=bool(form.remember.data))
    return jsonify(user.serialize()), 200


@auth_view.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return jsonify({'status': 'success'}), 200


@auth_view.route('/me', methods=['GET'])
def me():
    if not current_user.is_authenticated:
        return jsonify({'message': 'Unauthorized HTTP responses'}), 401

    return jsonify(current_user.serialize()), 200


@auth_view.route('/force-login', methods=['GET'])
def force_login():
    user = User.find(1)
    if user:
        login_user(user, True)

    return jsonify({'status': 'success'}), 200
