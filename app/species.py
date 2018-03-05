from .addons import db, ma

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify

class Species(db.Model):
    """This class represents the races table.
    Race is used to design our pet game and is not modifiable by the user."""

    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    #color = db.Column(ColorType)  # some visible attribute for user & designers
    #happy_range = db.Column(NumericRangeType)
    happy_rate = db.Column(db.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True))
    #hunger_range = db.Column(NumericRangeType)
    hunger_rate = db.Column(db.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True))

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
        return Species.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Race: {}>".format(self.name)


class SpeciesSchema(ma.ModelSchema):
    class Meta:
        model = Species
    animals = ma.HyperlinkRelated('animals')


species_schema = SpeciesSchema()
# species_schema = SpeciesSchema(many=True)


def species():
    all_users = Species.get_all()
    result = species_schema.dump(all_users, many=True)
    return jsonify(result.data)


def species_detail(id):
    user = Species.query.get(id)
    return species_schema.jsonify(user)
# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/authors/42",
#         "collection": "/api/authors/"
#     }
# }

