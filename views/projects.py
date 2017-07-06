from flask import Blueprint, make_response, jsonify, request
from models.user import User
from helpers import int_from_request, prepare_sorting_params
from forms import ProjectForm
from models.company import Company
from models.project import Project
from elastic import Elastic
from underscore import _
from rq import Queue
from worker import conn

projects_view = Blueprint('projects_view', __name__)


@projects_view.route('/get_by_id/<int:id>', methods=["GET"])
def get_by_id(id):
    project = Project.find(id)
    if not project:
        return jsonify({'message': 'project not found'}), 404

    return jsonify(project.serialize()), 200


@projects_view.route('/get_list', methods=['GET'])
def get_list():
    page = int_from_request('page', 1)
    limit = int_from_request('limit', 10)
    sort, reverse = prepare_sorting_params(['title', 'price', 'id', 'company'], 'id')

    elastic = Elastic()
    result = elastic.search_project()
    ids = _.pluck(result['hits']['hits'],'_id')

    projects = Project.where_in('projects.id',ids)\
        .select('projects.*','c.name as company')\
        .left_join('companies as c','c.id','=','projects.company_id')\
        .order_by(sort, reverse)\
        .paginate(limit, page)

    response = {
        'count': projects.total,
        'data': projects.serialize()
    }

    return jsonify(response), 200


@projects_view.route('/autocomplete', methods=["GET"])
def search():
    elastic = Elastic()
    result = elastic.autocomplete_project()
    return jsonify(result['hits']), 200


@projects_view.route('/geo_search', methods=["GET"])
def geo_search():
    elastic = Elastic()
    result = elastic.geo_search_project()

    return jsonify(result['hits']), 200


@projects_view.route('/create', methods=["POST"])
def create():
    form = ProjectForm(request.form)
    form.company_id.choices = [(str(c.id), str(c.id)) for c in Company.select('id').get()]
    if not form.validate():
        return jsonify(form.errors), 400

    project = Project.create({
        "title": form.data.get('title'),
        "description": str(form.data.get('description', '')),
        "price": round(form.data.get('price'), 2),
        "longitude": form.data.get('longitude'),
        "latitude": form.data.get('latitude'),
        "published": form.data.get('published'),
        "company_id": form.data.get('company_id'),
    })

    # Sync in Elastic
    elastic = Elastic()
    elastic.sync_project_document(project)

    return jsonify(project.serialize()), 200


@projects_view.route('/update/<int:id>', methods=["PUT"])
def update(id):

    project = Project.find(id)
    if not project:
        return jsonify({'message': 'project not found'}), 404

    form = ProjectForm.from_json(request.get_json())
    form.company_id.choices = [(str(c.id), str(c.id)) for c in Company.select('id').get()]
    if not form.validate():
        return jsonify(form.errors), 400

    project.title = form.data.get('title')
    project.description = form.data.get('description', '') if form.data.get('description', '') else ''
    project.price = round(form.data.get('price'), 2)
    project.longitude = form.data.get('longitude')
    project.latitude = form.data.get('latitude')
    project.published = bool(form.data.get('published'))
    project.company_id = form.data.get('company_id')
    project.save()

    # Sync in Elastic
    elastic = Elastic()
    elastic.sync_project_document(project)

    return jsonify(project.serialize()), 200


@projects_view.route('/delete/<int:id>', methods=["DELETE"])
def delete(id):
    project = Project.find(id)
    if not project:
        return jsonify({'message': 'project not found'}), 404

    project.delete()
    elastic = Elastic()
    elastic.delete_project_document(id)

    return jsonify({'message': 'project successfully deleted'}), 200

@projects_view.route('/sync', methods=["GET"])
def sync():
    elastic = Elastic()
    projects = Project.all()
    for project in projects:
        elastic.sync_project_document(project)

    return jsonify({'message': 'projects successfully sync to elastic'}), 200

@projects_view.route('/test_queue', methods=["GET"])
def test_queue():
    q = Queue('low',connection=conn)
    job = q.enqueue(test_job, args=('Andy Smolyar',))
    q = Queue('high', connection=conn)
    job = q.enqueue(test_job, args=('High Andy',))
    return "Success Test Job"


def test_job(name):
    user = User.find(1)
    user.username = name
    user.save()