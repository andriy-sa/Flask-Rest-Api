import app
import os
from werkzeug.contrib.fixers import ProxyFix
from app import socketio

mode = os.getenv('FLASK_MODE','development')
application = app.create_app(mode)

application.wsgi_app = ProxyFix(application.wsgi_app)

if __name__ == "__main__":
    socketio.run(application, debug=True)
