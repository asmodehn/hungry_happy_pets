from .addons import db, ma

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify


class Animal(db.Model):
    """This class represents the animals table."""

    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    happy = db.Column(db.Integer())
    hungry = db.Column(db.Integer())

    # authoring
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name."""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Animal.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Animal: {}>".format(self.name)



class AnimalSchema(ma.Schema):
    class Meta:
        model = Animal
    author = ma.HyperlinkRelated('owner')


animal_schema = AnimalSchema()
#animals_schema = UserSchema(many=True)


def animals():
    all_animals = Animal.all()
    result = animal_schema.dump(all_animals, many=True)
    return jsonify(result.data)


def animals_detail(id):
    animal = Animal.query.get(id)
    return animal_schema.jsonify(animal)
# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/authors/42",
#         "collection": "/api/authors/"
#     }
# }
