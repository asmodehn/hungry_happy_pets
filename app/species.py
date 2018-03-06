try:
    from .addons import db, ma
    from .animals import Animal
except SystemError:  # in case we call this module directly (doctest)
    from addons import db, ma
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

    >>> import users, owners  #import other modules to resolve relationships
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


class SpeciesSchema(ma.ModelSchema):
    """
    Usage through marshmallow-sqlalchemy:
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:')
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import users, owners  #import other modules to resolve relationships
    >>> Species.metadata.create_all(engine)

    >>> species_data = Species(name='testspecies', happy_rate=5, hunger_rate=23)
    >>> session.add(species_data)
    >>> session.commit()
    >>> session.query(Species).all()
    [<Species: testspecies>]

    >>> dump_data = species_schema.dump(species_data).data
    >>> import pprint  #ordering dict output
    >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
    {'happy_rate': 5, 'hunger_rate': 23, 'id': 1, 'name': 'testspecies'}

    >>> species_schema.load(dump_data, session=session).data
    <Species: testspecies>
    """
    class Meta:
        fields = ('id', 'name', 'happy_rate', 'hunger_rate')
        dump_only = ('id', )
        model = Species

    # author = ma.Nested(AuthorSchema)

    # links = ma.Hyperlinks({
    #     'self': ma.URLFor('book_detail', id='<id>'),
    #     'collection': ma.URLFor('book_list')
    # })
    #     model = Species
    #members = ma.HyperlinkRelated('members')



species_schema = SpeciesSchema()
# species_schema = SpeciesSchema(many=True)



def species():
    all_species = Species.all()
    user_dict, errors = species_schema.dump(all_species, many=True)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def species_read(id):
    species = Species.query.get(id)
    if not species:
        return '', http.HTTPStatus.NOT_FOUND
    species_dict, errors = species_schema.dump(species)
    if not errors:
        return species_dict
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


def species_edit(id):
    data = request.get_json()
    user = Species.query.get(id)

    if not user:
        return '', http.HTTPStatus.NOT_FOUND

    for k, v in data.items():
        setattr(user, k, v)

    species_dict, errors = species_schema.dump(user)
    if not errors:
        return species_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def species_add():
    data = request.get_json()
    user, errors = species_schema.load(data, )
    if not errors:
        user.save()

    user_dict, errors = species_schema.dump(user)
    if not errors:
        return user_dict, http.HTTPStatus.CREATED
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def species_delete(id):
    species = Species.query.get(id)
    if species:
        species.delete()
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
