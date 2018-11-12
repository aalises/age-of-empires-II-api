from db import db
from flask import request
from collections import OrderedDict
from api.models.factory import get_model

class CivilizationModel(db.Model):
    __tablename__ = 'civilizations'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=False)
    expansion = db.Column(db.String(80), nullable=False)
    army_type = db.Column(db.String(80), nullable=False)
    unique_unit = db.Column(db.String(80), db.ForeignKey('units.name'), nullable=False)
    unique_tech = db.Column(db.String(80), db.ForeignKey('technologies.name'), nullable=False)
    team_bonus = db.Column(db.String(200), nullable=False)
    civilization_bonus = db.Column(db.Text, nullable=False)

    unit = db.relationship('UnitModel', lazy='dynamic', uselist=True)
    technology = db.relationship('TechnologyModel', lazy='dynamic', uselist=True)

    def __init__(self, name, expansion, army_type,
                 unique_unit, unique_tech,
                 team_bonus, civilization_bonus):
        self.name = name
        self.expansion = expansion
        self.army_type = army_type
        self.unique_unit = unique_unit
        self.unique_tech = unique_tech
        self.team_bonus = team_bonus
        self.civilization_bonus = civilization_bonus

    def __repr__(self):
        return "<Civilization: {}>".format(self.name)

    def json(self):
        civilization = [('id', self._id),
                        ('name', self.name),
                        ('expansion', self.expansion),
                        ('army_type', self.army_type),
                        ('unique_unit', self.parse_array_field(self.unique_unit)
                         if not self.unit.first()
                         else ['{}unit/{}'.format(request.url_root + request.blueprint,
                                                  self.format_name_to_query(self.unit.first().name))]
                         ),
                        ('unique_tech', self.parse_array_field(self.unique_tech)
                         if not self.technology.first()
                         else ['{}technology/{}'.format(request.url_root + request.blueprint,
                               self.format_name_to_query(self.technology.first().name))]
                         ),
                        ('team_bonus', self.team_bonus),
                        ('civilization_bonus', self.civilization_bonus.split(";"))
                        ]
        return OrderedDict(civilization)

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

    def parse_array_field(self, field):
            out = []
            for item in [x for x in field.split(";")]:
                unit = get_model('units').query.filter_by(name=item).first()
                technology = get_model('technologies').query.filter_by(name=item).first()
                if unit:
                    out.append('{}unit/{}'.format(request.url_root + request.blueprint,
                                                  self.format_name_to_query(unit.name)))
                elif technology:
                    out.append('{}technology/{}'.format(request.url_root + request.blueprint,
                                                        self.format_name_to_query(technology.name)))
            return out
