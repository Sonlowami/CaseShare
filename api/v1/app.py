#!/usr/bin/python3
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flasgger import Swagger
from flasgger.utils import swag_from
from api.v1.views import api_views
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(api_views)
cors = CORS(app, resources={r"api/v1/*": {"origins": "*"}})

app.config['SWAGGER'] = {
    'title': 'CaseShare Swagger API',
    'uiversion': 3
}
Swagger(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
