from db import db
import json
from collections import OrderedDict
from flask import request

class UnitModel(db.Model):
    __tablename__ = 'units'

    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    expansion = db.Column(db.String(80), nullable=False)
    age = db.Column(db.String(80), nullable=False)
    created_in = db.Column(db.String(80), db.ForeignKey("structures.name"))
    cost = db.Column(db.String(80))
    build_time = db.Column(db.Integer)
    reload_time = db.Column(db.Float)
    attack_delay = db.Column(db.Float, nullable=True)
    movement_rate = db.Column(db.Float)
    line_of_sight = db.Column(db.Integer)
    hit_points = db.Column(db.Integer)
    range = db.Column(db.String(80), nullable=True)
    attack = db.Column(db.Integer)
    armor = db.Column(db.String(5))
    attack_bonus = db.Column(db.String(80), nullable=True)
    armor_bonus = db.Column(db.String(80), nullable=True)
    search_radius = db.Column(db.Integer, nullable=True)
    accuracy = db.Column(db.String(3), nullable=True)
    blast_radius = db.Column(db.Float, nullable=True)

    structure = db.relationship('StructureModel', lazy='dynamic', uselist=True)

    def __init__(self, name, description, expansion, age, created_in, cost, build_time,
                 reload_time, attack_delay, movement_rate, line_of_sight,
                 hit_points, range, attack, armor, attack_bonus=None,
                 armor_bonus=None, search_radius=None, accuracy=None,
                 blast_radius=None):
        self.name = name
        self.description = description
        self.expansion = expansion
        self.age = age
        self.created_in = created_in
        self.cost = cost
        self.build_time = int(build_time)
        self.reload_time = float(reload_time)
        self.attack_delay = float(attack_delay) if attack_delay else None
        self.movement_rate = float(movement_rate)
        self.line_of_sight = int(line_of_sight)
        self.hit_points = int(hit_points)
        self.range = range
        self.attack = int(attack)
        self.armor = armor
        self.attack_bonus = attack_bonus
        self.armor_bonus = armor_bonus
        self.search_radius = int(search_radius) if search_radius else None
        self.accuracy = accuracy
        self.blast_radius = float(blast_radius) if blast_radius else None

    def __repr__(self):
        return "<Unit: {}>".format(self.name)

    def json(self):
        unit = [('id', self._id), ('name', self.name),
                ('description', self.description),
                ('expansion', self.expansion),
                ('age', self.age),
                ('created_in',
                '{}structure/{}'.format(request.url_root + request.blueprint,
                                        self.format_name_to_query(self.structure.first().name))
                 if self.structure.first() else self.created_in),
                ('cost', json.loads(self.cost.replace(";", ","))),
                ('build_time', self.build_time),
                ('reload_time', self.reload_time),
                ('attack_delay', self.attack_delay),
                ('movement_rate', self.movement_rate),
                ('line_of_sight', self.line_of_sight),
                ('hit_points', self.hit_points),
                ('range', int(self.range) if self.range and self.range.isdigit() else self.range),
                ('attack', self.attack), ('armor', self.armor),
                ('attack_bonus', self.attack_bonus.split(";") if self.attack_bonus else None),
                ('armor_bonus', self.armor_bonus.split(";") if self.armor_bonus else None),
                ('search_radius', self.search_radius),
                ('accuracy', self.accuracy),
                ('blast_radius', self.blast_radius)]
        return OrderedDict([(k, v) for k, v in unit if v])

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
