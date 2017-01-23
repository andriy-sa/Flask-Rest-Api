from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
from flask_orator import Orator

from config import development, production, testing

app = Flask(__name__)


db = Orator()

login_manager = LoginManager()
bcrypt = Bcrypt()


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

    from views.default import default_view
    from views.users import users_view
    from views.companies import companies_view

    # Register Routes
    app.register_blueprint(users_view, url_prefix='/api/user')
    app.register_blueprint(companies_view, url_prefix='/api/company')
    # must register last one
    app.register_blueprint(default_view)

    return app

