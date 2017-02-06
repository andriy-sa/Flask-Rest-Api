from flask import Blueprint, make_response, jsonify, request
from models.project import Project
from helpers import int_from_request, prepare_sorting_params
from forms import ProjectForm
from models.company import Company
from models.project import Project
from elastic import Elastic

projects_view = Blueprint('projects_view', __name__)


@projects_view.route('/get_by_id/<int:id>', methods=["GET"])
def get_by_id(id):
    project = Project.find(id)
    if not project:
        return jsonify({'message': 'project not found'}), 404

    return jsonify(project.serialize()), 200


@projects_view.route('/search', methods=["GET"])
def search():
    elastic = Elastic()
    result = elastic.search_project()

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
        "description": form.data.get('description', ''),
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

    form = ProjectForm(request.form)
    form.company_id.choices = [(str(c.id), str(c.id)) for c in Company.select('id').get()]
    if not form.validate():
        return jsonify(form.errors), 400

    project.title = form.data.get('title')
    project.description = form.data.get('description', '')
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
