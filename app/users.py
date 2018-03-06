import http

try:
    from .addons import db, ma
except SystemError:  # in case we call this module directly (doctest)
    from addons import db, ma

from sqlalchemy_utils import PasswordType, EmailType, UUIDType  #,NumericRangeType
from flask import jsonify, request
from marshmallow import post_load


class User(db.Model):
    """This class represents the users table.
    User represent the generic concept of user of a service.

    >>> from addons import db
    >>> from mixer.backend.sqlalchemy import Mixer
    >>> engine = db.create_engine('sqlite:///:memory:')
    >>> Session = db.sessionmaker(bind=engine)

    >>> mixer = Mixer(session=Session(), commit=False)
    >>> user = mixer.blend('app.users.User', nick='testuser', email='tester@comp.any')
    >>> user
    <User: testuser>
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

    # def __init__(self, nick, email):
    #     """initialize with name."""
    #     self.nick = nick
    #     self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<User: {}>".format(self.nick)


class UserSchema(ma.Schema):

    """This class represents the users table.
    User represent the generic concept of user of a service.

    >>> from addons import db
    >>> from mixer.backend.marshmallow import Mixer
    >>> engine = db.create_engine('sqlite:///:memory:')
    >>> Session = db.sessionmaker(bind=engine)

    >>> mixer = Mixer(session=Session(), commit=False)
    >>> user = mixer.blend('app.users.UserSchema', nick='testuser', email='tester@comp.any')
    >>> user
    <User: testuser>

    # TODO : schema use as dict
    """

    class Meta:
        # Fields to expose
        fields = ('id', 'nick', 'email', 'date_created')
        exclude = ("password",)
        dump_only = ('id', )
        # Smart hyperlinking
        # _links = ma.Hyperlinks({
        #     'self': ma.URLFor('author_detail', id='<id>'),
        #     'collection': ma.URLFor('authors')
        # })

    @post_load
    def make_user(self, data):
        return User(**data)


user_schema = UserSchema()


def users():
    all_users = User.all()
    user_dict, errors = user_schema.dump(all_users, many=True)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def user_read(id):
    user = User.query.get(id)
    if not user:
        return '', http.HTTPStatus.NOT_FOUND
    user_dict, errors = user_schema.dump(user)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/authors/42",
#         "collection": "/api/authors/"
#     }
# }


def user_edit(id):
    data = request.get_json()
    user = User.query.get(id)

    if not user:
        return '', http.HTTPStatus.NOT_FOUND

    for k, v in data.items():
        setattr(user, k, v)

    user_dict, errors = user_schema.dump(user)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def user_add():
    data = request.get_json()
    user, errors = user_schema.load(data, )
    if not errors:
        user.save()

    user_dict, errors = user_schema.dump(user)
    if not errors:
        return user_dict, http.HTTPStatus.CREATED
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def user_delete(id):
    user = User.query.get(id)
    if user:
        user.delete()
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.NOT_FOUND

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


