import http

try:
    from .addons import db, ma
except SystemError:  # in case we call this module directly (doctest)
    from addons import db, ma

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify, request


class Owner(db.Model):
    """This class represents the owners table.
    Owner is needed to differentiate the user data (generic & widely used), with the owner data (specific to our app)

    >>> from addons import db
    >>> from mixer.backend.sqlalchemy import Mixer
    >>> engine = db.create_engine('sqlite:///:memory:')
    >>> Session = db.sessionmaker(bind=engine)

    >>> mixer = Mixer(session=Session(), commit=False)
    >>> user = mixer.blend('app.owners.Owner', nick='testuser', email='tester@comp.any')
    >>> user
    <User: testuser>
    """

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    #uuid = db.Column(UUIDType(binary=False))  # http://docs.sqlalchemy.org/en/rel_0_9/core/custom_types.html?highlight=guid#backend-agnostic-guid-type
    name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    pets = db.relationship('Animal', backref='owner', lazy=True)


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
        return Owner.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Owner: {}>".format(self.name)


class OwnerSchema(ma.Schema):
    class Meta:
        model = Owner

    #pets = ma.HyperlinkRelated('animals')

owner_schema = OwnerSchema()
#owners_schema = OwnerSchema(many=True)



def owners():
    all_users = Owner.get_all()
    user_dict, errors = owner_schema.dump(all_users, many=True)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def owner_read(id):
    user = Owner.query.get(id)
    if not user:
        return '', http.HTTPStatus.NOT_FOUND
    user_dict, errors = owner_schema.dump(user)
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


def owner_edit(id):
    data = request.get_json()
    owner = Owner.query.get(id)

    if not owner:
        return '', http.HTTPStatus.NOT_FOUND

    for k, v in data.items():
        setattr(owner, k, v)

    user_dict, errors = owner_schema.dump(owner)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def owner_add():
    data = request.get_json()
    owner, errors = owner_schema.load(data, )
    if not errors:
        owner.save()

    owner_dict, errors = owner_schema.dump(owner)
    if not errors:
        return owner_dict, http.HTTPStatus.CREATED
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def owner_delete(id):
    owner = Owner.query.get(id)
    if owner:
        owner.delete()
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.NOT_FOUND

