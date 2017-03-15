from flask import Flask
from flask_orator import Orator
import redis
from rq import Worker, Queue, Connection
from config import development

listen = ['high','medium','low']

redis_url = 'redis://localhost:6379'

conn = redis.from_url(redis_url)

app = Flask(__name__)
app.config.from_object(development)
db = Orator(app)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
