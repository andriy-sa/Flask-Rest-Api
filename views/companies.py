from flask import Blueprint, make_response, jsonify, request
from models.company import Company
from helpers import int_from_request, prepare_sorting_params
from forms import CompanyForm
from decorators import login_required
from werkzeug.datastructures import CombinedMultiDict

companies_view = Blueprint('companies_view', __name__)


@companies_view.route('/get_by_id/<int:id>', methods=["GET"])
def get_by_id(id):
    company = Company.find(id)
    if not company:
        return make_response(jsonify({'message': 'company not gound'})), 404

    return jsonify(company.serialize()), 200


@companies_view.route('/get_list', methods=['GET'])
@login_required(is_admin=True)
def get_list():
    page = int_from_request('page', 1)
    limit = int_from_request('limit', 10)

    sort_list = ['created_at', 'name']
    sort, reverse = prepare_sorting_params(sort_list, 'created_at')

    companies = Company.order_by(sort, reverse).paginate(limit, page)

    response = {
        'count': companies.total,
        'data': companies.serialize()
    }

    return jsonify(response), 200


@companies_view.route('/create', methods=['POST'])
def create():
    request_data = CombinedMultiDict((request.files, request.form))

    form = CompanyForm(request_data)
    if not form.validate():
        return jsonify(form.errors), 400

    company = Company.create({
        'name': form.data.get('name'),
        'address': form.data.get('address'),
        'logo': form.upload_logo() if form.logo.data else ''
    })

    return jsonify(company.serialize()), 200


@companies_view.route('/update/<int:id>', methods=['PUT'])
def update(id):
    company = Company.find(id)
    if not company:
        return make_response(jsonify({'message': 'company not gound'})), 404

    request_data = CombinedMultiDict((request.files, request.form))
    form = CompanyForm(request_data)
    if not form.validate():
        return jsonify(form.errors), 400

    company.name = form.data.get('name')
    company.address = form.data.get('address')
    if form.logo.data:
        if company.logo:
            form.remove_logo(company.logo)

        company.logo = form.upload_logo()

    company.save()

    return jsonify(company.serialize()), 200
