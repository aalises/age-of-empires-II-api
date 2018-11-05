from flask import Flask, Blueprint, redirect
from flask_restful import Api
from sqlalchemy_utils import database_exists
from config import APP_CONFIG, API_PREFIX, DB_NAME
from api.resources.civilization import Civilization, CivilizationList
from api.resources.unit import Unit, UnitList
from api.resources.structure import Structure, StructureList
from api.resources.technology import Technology, TechnologyList
from db.populate_tables import populate_db
from db.db import db


app = Flask(__name__)
app.config.update(APP_CONFIG)

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint, prefix=API_PREFIX)

# Routes of our application
api.add_resource(Civilization, '/civilization/<string:_id>')
api.add_resource(CivilizationList, '/civilizations')
api.add_resource(Unit, '/unit/<string:_id>')
api.add_resource(UnitList, '/units')
api.add_resource(Structure, '/structure/<string:_id>')
api.add_resource(StructureList, '/structures')
api.add_resource(Technology, '/technology/<string:_id>')
api.add_resource(TechnologyList, '/technologies')

app.register_blueprint(api_blueprint)
db.init_app(app)

@app.before_first_request
def create_tables():
    if not database_exists(DB_NAME):
        db.create_all()
        populate_db()

@app.route(API_PREFIX)
@app.route("/")
def redirect_to_civilizations():
    return redirect("{}/civilizations".format(API_PREFIX), code=302)


if __name__ == "__main__":
    app.run(port=5000, debug=True, host='0.0.0.0')
