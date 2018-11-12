from db import db
import json
from collections import OrderedDict
from api.models.factory import get_model


from flask import request


class TechnologyModel(db.Model):
    __tablename__ = 'technologies'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(80), nullable=True)
    expansion = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    develops_in = db.Column(db.String(80), db.ForeignKey("structures.name"), nullable=False)
    cost = db.Column(db.String(80), nullable=False)
    build_time = db.Column(db.Integer, nullable=False)
    applies_to = db.Column(db.String(80), nullable=True)

    structure = db.relationship('StructureModel', lazy='dynamic', uselist=True)

    def __init__(self, name, expansion, age, develops_in, cost, build_time, applies_to, description):
        self.name = name
        self.description = description
        self.expansion = expansion
        self.age = age
        self.develops_in = develops_in
        self.cost = cost
        self.build_time = int(build_time) if build_time else None
        self.applies_to = applies_to

    def __repr__(self):
        return "<Technology: {}>".format(self.name)

    def json(self):
        technology = [('id', self._id),
                      ('name', self.name),
                      ('description', self.description),
                      ('expansion', self.expansion),
                      ('age', self.age),
                      ('develops_in',
                      '{}structure/{}'.format(request.url_root + request.blueprint, self.format_name_to_query(self.structure.first().name))
                       if self.structure.first() else self.develops_in),
                      ('cost', json.loads(self.cost.replace(";", ","))),
                      ('build_time', self.build_time),
                      ('applies_to', self.map_to_resource_url() if self.applies_to else None),
                      ]
        return OrderedDict([(k, v) for k, v in technology if v])

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(_id=id).first()

    @classmethod
    def find_by_name(cls, name):
        name = cls.format_name_to_display(name)
        return cls.query.filter_by(name=name).first()

    @classmethod
    def format_name_to_display(cls, name):
        formatted_name = name.replace("_", " ").replace("-", " ").split()
        return " ".join([x.capitalize() for x in formatted_name])

    def format_name_to_query(self, name):
        formatted_name = name.replace(" ", "_").replace(" ", "_").split()
        return "_".join([x.lower() for x in formatted_name])

    def map_to_resource_url(self):
        out = []
        for item in self.applies_to.split(';'):
            unit = get_model('units').query.filter_by(name=item).first()
            structure = get_model('structures').query.filter_by(name=item).first()
            civilization = get_model('civilizations').query.filter_by(name=item).first()

            if unit:
                out.append('{}unit/{}'.format(request.url_root + request.blueprint, self.format_name_to_query(unit.name)))
            elif structure:
                out.append('{}structure/{}'.format(request.url_root + request.blueprint, self.format_name_to_query(structure.name)))
            elif civilization:
                out.append('{}civilization/{}'.format(request.url_root + request.blueprint, self.format_name_to_query(civilization.name)))
            else:
                out.append(item)
        return out
