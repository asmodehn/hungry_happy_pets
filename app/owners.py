try:
    from .addons import db, ma
    from .animals import Animal, AnimalSchema
except SystemError:  # in case we call this module directly (doctest)
    from addons import db, ma
    from animals import Animal, AnimalSchema

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


class OwnerSchema(ma.ModelSchema):
    """
    Usage through marshmallow-sqlalchemy :
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import users  #import other modules to resolve relationships
    >>> Owner.metadata.create_all(engine)

    >>> owner_data = Owner()
    >>> owner_data.user = users.User(nick='testuser', email='tester@comp.any')

    >>> session.add(owner_data)
    >>> session.commit()
    >>> session.query(Owner).all()
    [<Owner: <User: testuser> []>]

    >>> dump_data = owner_schema.dump(owner_data).data
    >>> import pprint  #ordering dict output
    >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
    {'date_created': '...',
     'date_modified': '...',
     'id': 1,
     'pets': []}

    >>> owner_schema.load(dump_data, session=session).data
    <Owner: <User: testuser> []>
    """


    class Meta:
        # fields = ('id', 'user_id')
        # dump_only = ('id',)
        model = Owner

    #ma.fields.Nested(UserSchema, only=["nick", "email"])
    #fields.Nested(AnimalSchema, only=["name", "species"])

    #pets = ma.HyperlinkRelated('animals')

    # links = ma.Hyperlinks({
    #     'self': ma.URLFor('book_detail', id='<id>'),
    #     'collection': ma.URLFor('book_list')
    # })
    #     model = Species
    #members = ma.HyperlinkRelated('members')


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


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)