from flask import Flask, g
from flask_orator import Orator

from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import settings

app = Flask(__name__)
app.config.from_object(settings)

db = Orator(app)

login_manager = LoginManager(app)
bcrypt = Bcrypt(app)


@app.before_request
def _before_reques():
    g.user = current_user
