from flask import Flask, redirect
from flask_restful import Api
from sqlalchemy_utils import database_exists

from resources.civilization import Civilization, CivilizationList
from resources.unit import Unit, UnitList
from resources.structure import Structure, StructureList
from resources.technology import Technology, TechnologyList
from populate_tables import populate_db
from db import db

DB_NAME = 'sqlite:///data.db'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['JSON_SORT_KEYS'] = False

api = Api(app)

db.init_app(app)


@app.before_first_request
def create_tables():
    if not database_exists(DB_NAME):
        db.create_all()
        populate_db()


api.add_resource(Civilization, '/civilization/<string:_id>')
api.add_resource(CivilizationList, '/civilizations')

api.add_resource(Unit, '/unit/<string:_id>')
api.add_resource(UnitList, '/units')

api.add_resource(Structure, '/structure/<string:_id>')
api.add_resource(StructureList, '/structures')

api.add_resource(Technology, '/technology/<string:_id>')
api.add_resource(TechnologyList, '/technologies')


@app.route('/')
def redirect_to_civilizations():
    return redirect("/civilizations", code=302)


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
