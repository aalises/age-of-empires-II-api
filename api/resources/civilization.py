from flask_restful import Resource
from api.models.civilization import CivilizationModel
from flask import jsonify

class Civilization(Resource):
    def get(self, _id):
        civilization = None
        if _id.isdigit():
            civilization = CivilizationModel.find_by_id(_id)
        else:
            civilization = CivilizationModel.find_by_name(_id)

        if civilization:
            return jsonify(civilization.json())
        return {'message': 'Civilization not found'}, 404


class CivilizationList(Resource):
    def get(self):
        return jsonify({'civilizations': list(map(lambda x: x.json(),
                        CivilizationModel.query.all()))})
