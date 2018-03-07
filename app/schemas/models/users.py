try:
    from ._bootstrap import db
    from .owners import Owner
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import db
    from owners import Owner


from sqlalchemy_utils import PasswordType, EmailType, UUIDType  #,NumericRangeType
from flask import jsonify, request
from marshmallow import post_load


class User(db.Model):
    """This class represents the users table.
    User represent the generic concept of user of a service.

    Usage through sqlalchemy :
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:')
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import species  #import other modules to resolve relationships
    >>> User.metadata.create_all(engine)
    >>> user_data = User(nick='testuser', email='tester@comp.any')
    >>> session.add(user_data)
    >>> session.commit()
    >>> session.query(User).all()
    [<User: testuser>]
    """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    #uuid = db.Column(UUIDType(binary=False))  # http://docs.sqlalchemy.org/en/rel_0_9/core/custom_types.html?highlight=guid#backend-agnostic-guid-type
    nick = db.Column(db.String)
    email = db.Column(EmailType())  # TODO : support multiple with primary contact point (github style)
    password = db.Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
        ],
    ))
    designer = db.Column(db.Boolean)  # whether this user is also a designer and can edit the races table
    owners = db.relationship('Owner', backref='user', lazy=True)

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

    def save(self, session=None):
        """
        save the data
        :param session: optional in case flask has not been initialized
        :return:
        """
        if session is None:
            session = db.session
        session.add(self)
        session.commit()

    @staticmethod
    def all():
        return User.query.all()

    def delete(self, session=None):
        if session is None:
            session = db.session
        session.delete(self)
        session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.nick)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


