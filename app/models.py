from flask_sqlalchemy import SQLAlchemy

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType, NumericRangeType

# initialize sql-alchemy
db = SQLAlchemy()


# DB design :
# Users 1-1 Owner
# Animals *-1 Race
# Animals *-1 Owner
# TODO : nice entity association ascii art

class User(db.Model):
    """This class represents the users table.
    User represent the generic concept of user of a service.
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType(binary=False))  # http://docs.sqlalchemy.org/en/rel_0_9/core/custom_types.html?highlight=guid#backend-agnostic-guid-type
    nick = db.Column(db.String)
    email = db.Column(EmailType())  # TODO : support multiple with primary contact point (github style)
    password = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
        ],
    ))
    designer = db.Column(db.Boolean)  # wether this user is also a designer and can edit the races table

    # authoring
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, nick, email):
        """initialize with name."""
        self.nick = nick
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.name)



class Owner(db.Model):
    """This class represents the owners table.
    Owner is needed to differentiate the user data (generic & widely used), with the owner data (specific to our app)
    """

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(UUIDType(binary=False))  # http://docs.sqlalchemy.org/en/rel_0_9/core/custom_types.html?highlight=guid#backend-agnostic-guid-type
    name = db.Column(db.String)


    # authoring
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, nick, email):
        """initialize with name."""
        self.nick = nick
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Owner: {}>".format(self.name)



class Race(db.Model):
    """This class represents the races table.
    Race is used to design our pet game and is not modifiable by the user."""

    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    color = db.Column(ColorType)  # some visible attribute for user & designers
    happy_range = db.Column(NumericRangeType)
    happy_rate = db.Column(db.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True))
    hunger_range = db.Column(NumericRangeType)
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
        return Race.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Race: {}>".format(self.name)


class Animal(db.Model):
    """This class represents the animals table."""

    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    happy = db.Column(db.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True))
    hungry = db.Column(db.Numeric(precision=None, scale=None, decimal_return_scale=None, asdecimal=True))

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
