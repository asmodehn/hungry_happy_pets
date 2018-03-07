try:
    from ._bootstrap import db
    from .animals import Animal
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import db
    from animals import Animal

import http
from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify, request
from marshmallow import fields, post_load


class Owner(db.Model):
    """This class represents the owners table.
    Owner is needed to differentiate the user data (generic & widely used), with the owner data (specific to our app)

    Usage through sqlalchemy :
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import users, species  #import other modules to resolve relationships
    >>> Owner.metadata.create_all(engine)

    >>> owner_data = Owner()
    >>> owner_data.user = users.User(nick='testuser', email='tester@comp.any')

    >>> session.add(owner_data)
    >>> session.commit()
    >>> session.query(Owner).all()
    [<Owner: <User: testuser> []>]

    # TODO get rid of mixer, makes things less obvious => pure sqlalchemy

    """

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    #uuid = db.Column(UUIDType(binary=False))  # http://docs.sqlalchemy.org/en/rel_0_9/core/custom_types.html?highlight=guid#backend-agnostic-guid-type
    #name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pets = db.relationship('Animal', backref='owner', lazy=True)


    # authoring
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    # https://github.com/klen/mixer#support-for-flask-sqlalchemy-models-that-have-init-arguments
    # def __init__(self, nick, email):
    #     """initialize with name."""
    #     self.nick = nick
    #     self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Owner.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Owner: {} {}>".format(self.user, self.pets)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)