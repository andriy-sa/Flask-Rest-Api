from flask import Blueprint, make_response, jsonify, request
from models.user import User
from helpers import int_from_request, prepare_sorting_params

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
