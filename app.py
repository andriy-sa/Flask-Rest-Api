from flask import Flask, g, jsonify
from flask_bcrypt import Bcrypt
from flask_orator import Orator
from flask_elasticsearch import FlaskElasticsearch
import click
from config import development, production, testing
from flask_socketio import SocketIO
import wtforms_json
from helpers import jwt, get_jwt_user

app = Flask(__name__)

db = Orator()
bcrypt = Bcrypt()
es = FlaskElasticsearch()


socketio = SocketIO(app, async_mode='eventlet')


@app.before_request
def _before_reques():
    g.user = get_jwt_user()


@app.after_request
def _after_request(response):
    response.headers["Access-Control"] = "*"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "X-REQUESTED-WITH, CONTENT-TYPE, ACCEPT, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, HEAD, OPTIONS"
    response.headers["Access-Control-Expose-Headers"] = "CONTENT-TYPE, X-DEPRECATED"

    return response


@app.route('/api/reports', methods=['GET', 'POST'])
def index(id=None):
    return jsonify(success=True), 200


def create_app(type='development'):
    if type == 'development':
        app.config.from_object(development)
    elif type == 'production':
        app.config.from_object(production)
    elif type == 'testing':
        app.config.from_object(testing)

    db.init_app(app)
    bcrypt.init_app(app)
    es.init_app(app)
    wtforms_json.init()

    from views.default import default_view
    from views.users import users_view
    from views.companies import companies_view
    from views.projects import projects_view
    from views.auth import auth_view
    from models.user import authenticate, identity

    jwt.identity_handler(identity)
    jwt.authentication_handler(authenticate)
    jwt.init_app(app)

    # Register Routes
    app.register_blueprint(auth_view, url_prefix='/api')
    app.register_blueprint(users_view, url_prefix='/api/user')
    app.register_blueprint(companies_view, url_prefix='/api/company')
    app.register_blueprint(projects_view, url_prefix='/api/project')
    # must register last one
    app.register_blueprint(default_view)

    app.status = True

    return app


@app.cli.command()
def create_elastic_index():
    """Initialize ElasticSearch Index."""
    index = 'test_index'
    if es.indices.exists(index):
        es.indices.delete(index=index)
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1,
            "analysis": {
                "filter": {
                    "autocomplete_filter": {
                        "type": "edge_ngram",
                        "min_gram": 3,
                        "max_gram": 50
                    }
                },
                "analyzer": {
                    "autocomplete": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "filter": [
                            "lowercase",
                            "autocomplete_filter"
                        ]
                    }
                }
            }
        },
        "mappings": {
            "projects": {
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "title": {
                        "type": "string",
                        "analyzer": "autocomplete"
                    },
                    "description": {
                        "type": "string",
                    },
                    "price": {
                        "type": "double"
                    },
                    "published": {
                        "type": "boolean"
                    },
                    "location": {
                        "type": "geo_point"
                    },
                    "created_at": {
                        "type": "string",
                        "index": "no"
                    }
                }
            }
        }
    }
    # create index
    res = es.indices.create(index=index, ignore=400, body=settings)
    click.echo('Index created')

@app.cli.command()
def test_com():
    click.echo('test_com')
