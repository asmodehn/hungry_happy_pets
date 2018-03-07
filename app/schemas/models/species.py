try:
    from ._bootstrap import db
    from .animals import Animal
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import db
    from animals import Animal


import http

from marshmallow import post_load

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify, request


class Species(db.Model):
    """This class represents the races table.
    Species is used to design our pet game and is not modifiable by the user.

    Usage through sqlalchemy :
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:')
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import users, owners, animals  #import other modules to resolve relationships
    >>> Species.metadata.create_all(engine)
    >>> species_data = Species(name='testspecies', happy_rate=5, hunger_rate=23)
    >>> session.add(species_data)
    >>> session.commit()
    >>> session.query(Species).all()
    [<Species: testspecies>]
    """

    __tablename__ = 'species'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    #TODO color = db.Column(ColorType)  # some visible attribute for user & designers
    #happy_range = db.Column(NumericRangeType)
    #happy_rate = db.Column(db.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True))
    happy_rate = db.Column(db.Integer())  # avoiding float issues
    #hunger_range = db.Column(NumericRangeType)
    #hunger_rate = db.Column(db.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True))
    hunger_rate = db.Column(db.Integer())  # avoiding float issues

    members = db.relationship('Animal', backref='species', lazy=True)

    # authoring
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    #https://github.com/klen/mixer#support-for-flask-sqlalchemy-models-that-have-init-arguments
    # def __init__(self, name):
    #     """initialize with name."""
    #     self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all():
        return Species.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Species: {}>".format(self.name)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
