from flask import Blueprint, render_template

default_view = Blueprint('default_view', __name__)


@default_view.route("/")
@default_view.route("/<path:path>")
def index(path=None):
    return render_template('main.html')
