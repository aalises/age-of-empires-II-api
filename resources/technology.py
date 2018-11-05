from flask_restful import Resource
from models.technology import TechnologyModel


class Technology(Resource):
    def get(self, _id):
        technology = None
        if _id.isdigit():
            technology = TechnologyModel.find_by_id(_id)
        else:
            technology = TechnologyModel.find_by_name(_id)
        if technology:
            return technology.json()
        return {'message': 'Technology not found'}, 404


class TechnologyList(Resource):
    def get(self):
        return {'technologies': list(map(lambda x: x.json(),
                TechnologyModel.query.all()))}
