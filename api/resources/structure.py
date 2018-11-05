from flask_restful import Resource
from api.models.structure import StructureModel
from flask import jsonify

class Structure(Resource):
    def get(self, _id):
        structure = None
        if _id.isdigit():
            structure = StructureModel.find_by_id(_id)
        else:
            structure = StructureModel.find_by_name(_id)

        if structure:
            return jsonify(structure[0].json()) if len(structure) == 1 else jsonify(list(map(lambda x: x.json(), structure)))
        else:
            return {'message': 'Structure not found'}, 404


class StructureList(Resource):
    def get(self):
        return jsonify({'structures': list(map(lambda x: x.json(),
                        StructureModel.query.all()))})
