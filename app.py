from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_orator import Orator
from flask_elasticsearch import FlaskElasticsearch
import click
from config import development, production, testing

app = Flask(__name__)

db = Orator()

login_manager = LoginManager()
bcrypt = Bcrypt()
es = FlaskElasticsearch()


@app.before_request
def _before_reques():
    g.user = current_user


def create_app(type='development'):
    if type == 'development':
        app.config.from_object(development)
    elif type == 'production':
        app.config.from_object(production)
    elif type == 'testing':
        app.config.from_object(testing)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    es.init_app(app)

    from views.default import default_view
    from views.users import users_view
    from views.companies import companies_view
    from views.auth import auth_view

    # Register Routes
    app.register_blueprint(auth_view, url_prefix='/api')
    app.register_blueprint(users_view, url_prefix='/api/user')
    app.register_blueprint(companies_view, url_prefix='/api/company')
    # must register last one
    app.register_blueprint(default_view)

    return app


@app.cli.command()
def create_elastic_index():
    """Initialize ElasticSearch Index."""
    index = 'test_index'
    if es.indices.exists(index):
        es.indices.delete(index=index)
    # index settings
    settings = {
        "mappings": {
            "projects": {
                "properties": {
                    "title": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "location": {
                        "type": "geo_point"
                    }
                }
            }
        }
    }
    # create index
    res = es.indices.create(index=index, ignore=400, body=settings)
    click.echo('Index created')


@app.cli.command()
def create_elastic_document():
    index = 'test_index'
    if es.exists(index=index, id=1, doc_type='projects'):
        res = es.update(index=index, id=1, doc_type='projects', body={"doc": {
            "title": "First project",
            "description": "Description of project",
            "location": "20,50"
        }})
        message = "Document updated"
    else:
        res = es.update(index=index, id=1, doc_type='projects', body={
            "title": "First project",
            "description": "Description of project",
            "location": "20,50"
        })
        message = "Document created"
    print(res)

    click.echo(message)
