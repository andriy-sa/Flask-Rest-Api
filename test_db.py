from flask import Flask
from config import testing
from flask_orator import Orator

app = Flask(__name__)
app.config.from_object(testing)

db = Orator(app)

if __name__ == '__main__':
    db.cli.run()
