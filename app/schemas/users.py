import http

try:
    from ._bootstrap import ma
    from .models import User
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import ma
    from models import User

from sqlalchemy_utils import PasswordType, EmailType, UUIDType  #,NumericRangeType
from flask import jsonify, request
from marshmallow import post_load



class UserSchema(ma.ModelSchema):

    """This class represents the users table.
    User represent the generic concept of user of a service.

    Usage through marshmallow-sqlalchemy:
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

    >>> dump_data = user_schema.dump(user_data).data
    >>> import pprint  #ordering dict output
    >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
    {'email': 'tester@comp.any', 'id': 1, 'nick': 'testuser'}

    >>> user_schema.load(dump_data, session=session).data
    <User: testuser>

    """

    class Meta:
        model = User

        # Fields to expose
        fields = ('id', 'nick', 'email')
        exclude = ("password",)
        dump_only = ('id', )
        # Smart hyperlinking
        # _links = ma.Hyperlinks({
        #     'self': ma.URLFor('author_detail', id='<id>'),
        #     'collection': ma.URLFor('authors')
        # })


user_schema = UserSchema()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


