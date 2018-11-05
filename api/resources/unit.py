from flask_restful import Resource
from api.models.unit import UnitModel
from flask import jsonify

class Unit(Resource):
    def get(self, _id):
        unit = None
        if _id.isdigit():
            unit = UnitModel.find_by_id(_id)
        else:
            unit = UnitModel.find_by_name(_id)
        if unit:
            return jsonify(unit.json())
        return {'message': 'Unit not found'}, 404


class UnitList(Resource):
    def get(self):
        return jsonify({'units': list(map(lambda x: x.json(),
                        UnitModel.query.all()))})
