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


load_dotenv()

app = Flask(__name__)
#talisman = Talisman(app)

app.url_map.strict_slashes = False
app.config.from_object(Config)
app.register_blueprint(api_views)
db.init_app(app)

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
    return response

app.config['SWAGGER'] = {
    'title': 'CaseShare Swagger API',
    'uiversion': 3
}
Swagger(app)

def test_client():
    return app.test_client()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = app.config['PORT'])
