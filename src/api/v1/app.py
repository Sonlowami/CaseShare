#!/usr/bin/python3
from flask import Flask, jsonify, render_template
from flasgger import Swagger
from api.v1.views import api_views
from utils.decorators import token_required
from flasgger import Swagger
from dotenv import load_dotenv
from utils.database import db
from utils.config import Config
from flask_talisman import Talisman
from flask_migrate import Migrate
from flask_cors import CORS
from utils.logger import logger
from flask_socketio import SocketIO
import eventlet
import eventlet.wsgi


load_dotenv()

app = Flask(__name__)
talisman = Talisman(app, force_https=False)
socketio = SocketIO(app, logger=True, engineio_logger=True)
migrate = Migrate(app, db)
#CORS(app)

app.url_map.strict_slashes = False
app.config.from_object(Config)
app.register_blueprint(api_views)
db.init_app(app)
logger.info('Connected to database successfully')

if app.config['CS_ENV'] == 'test':
    with app.app_context():
        db.drop_all()

with app.app_context():
    db.create_all()

@app.after_request
def add_cors_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Accepts,Authorization,x-token")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE")
    logger.info('Response sent')
    return response

@app.before_request
def before_request():
    logger.info('Request received')

app.config['SWAGGER'] = {
    'title': 'CaseShare Swagger API',
    'uiversion': 3
}
Swagger(app)

def test_client():
    client = app.test_client()
    client.environ_base['wsgi.url_scheme'] = 'https'
    return client

import api.v1.views.notification_handlers

if __name__ == '__main__':
    logger.info('Starting app...')
    socket = eventlet.listen(('127.0.0.1', app.config['PORT']))
    ssl_socket = eventlet.wrap_ssl(socket, certfile=app.config['CERT'], keyfile=app.config['KEY'], server_side=True)
    eventlet.wsgi.server(ssl_socket, app)