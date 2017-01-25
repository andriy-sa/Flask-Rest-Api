import app
import os

mode = os.getenv('FLASK_MODE','development')
application = app.create_app(mode)

if __name__ == "__main__":
    application.run()
