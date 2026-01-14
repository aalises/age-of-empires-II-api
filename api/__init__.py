from flask import Flask, Blueprint
from flask_restful import Api
from api.resources.civilization import Civilization, CivilizationList
from api.resources.unit import Unit, UnitList
from api.resources.structure import Structure, StructureList
from api.resources.technology import Technology, TechnologyList
from config import API_PREFIX, SWAGGER_CONFIG
from db import db
from flasgger import Swagger

def create_app(cfg):
        app = Flask(__name__)
        app.config.update(cfg)

        api_blueprint = Blueprint(API_PREFIX + "/", __name__)
        api = Api(api_blueprint, prefix="/" + API_PREFIX)

        add_routes(api)
        add_docs(app, SWAGGER_CONFIG, '../docs/apispecs.yaml')
        app.register_blueprint(api_blueprint)
        db.init_app(app)

        return app

def add_routes(api):
        # Routes of our application
        api.add_resource(Civilization, '/civilization/<string:_id>')
        api.add_resource(CivilizationList, '/civilizations')
        api.add_resource(Unit, '/unit/<string:_id>')
        api.add_resource(UnitList, '/units')
        api.add_resource(Structure, '/structure/<string:_id>')
        api.add_resource(StructureList, '/structures')
        api.add_resource(Technology, '/technology/<string:_id>')
        api.add_resource(TechnologyList, '/technologies')

def add_docs(app, cfg, template):
        Swagger(app, config=cfg, template_file=template)
