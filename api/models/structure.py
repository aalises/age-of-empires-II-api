from db import db
import json
from collections import OrderedDict

class StructureModel(db.Model):
    __tablename__ = 'structures'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    expansion = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    cost = db.Column(db.String(80), nullable=False)
    build_time = db.Column(db.Integer, nullable=False)
    hit_points = db.Column(db.Integer, nullable=False)
    line_of_sight = db.Column(db.Integer, nullable=False)
    armor = db.Column(db.String(5), nullable=False)
    range = db.Column(db.String(80), nullable=True)
    reload_time = db.Column(db.Float, nullable=True)
    attack = db.Column(db.Integer, nullable=True)
    special = db.Column(db.Text, nullable=True)

    def __init__(self, name, expansion, age, cost, build_time,
                 hit_points, line_of_sight, armor, range=None, reload_time=None,
                 attack=None, special=None):
        self.name = name
        self.expansion = expansion
        self.age = age
        self.cost = cost
        self.build_time = int(build_time)
        self.reload_time = float(reload_time) if reload_time else None
        self.hit_points = int(hit_points)
        self.line_of_sight = int(line_of_sight)
        self.range = range
        self.attack = int(attack) if attack else None
        self.armor = armor
        self.special = special

    def __repr__(self):
        return "<Structure: {}>".format(self.name)

    def json(self):
        structure = [('id', self._id),
                     ('name', self.name),
                     ('expansion', self.expansion),
                     ('age', self.age),
                     ('cost', json.loads(self.cost.replace(";", ","))),
                     ('build_time', self.build_time),
                     ('reload_time', self.reload_time),
                     ('hit_points', self.hit_points),
                     ('line_of_sight', self.line_of_sight),
                     ('range', int(self.range) if self.range and self.range.isdigit() else self.range),
                     ('attack', self.attack),
                     ('armor', self.armor),
                     ('special', self.special.split(";") if self.special else [])]
        return OrderedDict([(k, v) for k, v in structure if v])

    @classmethod
    def find_by_id(cls, id):
        return [cls.query.filter_by(_id=id).first()]

    @classmethod
    def find_by_name(cls, name):
        name = cls.format_name_to_display(name)
        return cls.query.filter_by(name=name).all()

    @classmethod
    def format_name_to_display(cls, name):
        formatted_name = name.replace("_", " ").replace("-", " ").split()
        return " ".join([x.capitalize() for x in formatted_name])
