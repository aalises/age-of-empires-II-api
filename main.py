from flask import redirect, jsonify, request
from sqlalchemy_utils import database_exists
from config import APP_CONFIG, API_PREFIX, DB_NAME
from api import create_app
from db.populate_tables import populate_db
from db import db
from collections import OrderedDict

app = create_app(APP_CONFIG)

@app.before_first_request
def create_tables():
    if not database_exists(DB_NAME):
        db.create_all()
        populate_db()

@app.route("/" + API_PREFIX)
def show_resources():
    resources = [('civilizations', '{}/civilizations'.format(request.url)),
                 ('units', '{}/units'.format(request.url)),
                 ('structures', '{}/structures'.format(request.url)),
                 ('technologies', '{}/technologies'.format(request.url))
                 ]
    return jsonify({'resources': OrderedDict(resources)})

@app.route("/")
def redirect_to_docs():
    return redirect("docs/", code=302)


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
