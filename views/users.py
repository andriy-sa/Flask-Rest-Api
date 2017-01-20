from flask import Blueprint, make_response, jsonify, request
from models.user import User
from helpers import int_from_request, prepare_sorting_params
from forms import UserForm, UserUpdateForm

users_view = Blueprint('users_view', __name__)


@users_view.route('/get_by_id/<int:id>', methods=["GET"])
def get_user_by_id(id):
    user = User.with_('company').find(id)
    if not user:
        return make_response(jsonify({'message': 'user not found'})), 404

    return user.to_json(), 200


@users_view.route('/get_list', methods=["GET"])
def get_list():
    page = int_from_request('page', 1)
    limit = int_from_request('limit', 10)

    sort_list = ['created_at', 'username']
    sort, reverse = prepare_sorting_params(sort_list, 'created_at')

    users = User.with_('company').order_by(sort, reverse).paginate(limit, page)

    response = {
        'count': users.total,
        'data': users.serialize()
    }

    return jsonify(response), 200


@users_view.route('/get_by_company/<int:id>', methods=['GET'])
def get_by_company(id):
    page = int_from_request('page', 1)
    limit = int_from_request('limit', 10)

    sort_list = ['created_at', 'username']
    sort, reverse = prepare_sorting_params(sort_list, 'created_at')

    users = User.where('company_id', id).order_by(sort, reverse).paginate(limit, page)

    response = {
        'count': users.total,
        'data': users.serialize()
    }

    return jsonify(response), 200


@users_view.route('/create', methods=['POST'])
def create():
    form = UserForm(request.form)
    if not form.validate():
        return jsonify(form.errors), 400

    user = User()
    user.username = form.data.get('username')
    user.email = form.data.get('email')
    user.password = User.make_password(form.data.get('password'))
    user.company_id = form.data.get('company_id')
    user.first_name = form.data.get('first_name','')
    user.last_name = form.data.get('last_name','')
    user.country = form.data.get('country','')
    user.city = form.data.get('city','')
    user.phone = form.data.get('phone','')
    user.save()

    return user.to_json(), 200


@users_view.route('/update/<int:id>', methods=['PUT'])
def update(id):
    user = User.find(id)
    if not user:
        return make_response(jsonify({'message': 'user not found'})), 404

    form = UserUpdateForm(request.form)
    form.set_user_id(id)

    if not form.validate():
        return jsonify(form.errors), 400

    user.username = form.data.get('username')
    user.email = form.data.get('email')
    user.company_id = form.data.get('company_id')
    user.first_name = form.data.get('first_name', '')
    user.last_name = form.data.get('last_name', '')
    user.country = form.data.get('country', '')
    user.city = form.data.get('city', '')
    user.phone = form.data.get('phone', '')
    user.save()

    return user.to_json(), 200


