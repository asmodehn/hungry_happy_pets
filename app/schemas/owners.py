try:
    from ._bootstrap import ma
    from .models import Owner
    from .animals import AnimalSchema
    from .users import UserSchema
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import ma
    from models import Owner
    from animals import AnimalSchema
    from users import UserSchema

import http
from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify, request
from marshmallow import fields, post_load


class OwnerSchema(ma.ModelSchema):
    """
    Usage through marshmallow-sqlalchemy :
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:', echo=False)
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import models, users, species, animals  #import other modules to resolve relationships
    >>> Owner.metadata.create_all(engine)

    >>> user_data, user_errors = users.user_schema.load({'nick': 'testuser', 'email': 'tester@comp.any'}, session=session)
    >>> user_data
    <User: testuser>

    >>> user_data.save(session=session)
    >>> session.query(users.User).all()
    [<User: testuser>]

    >>> species_data, species_errors = species.species_schema.load({'name': 'testspecies', 'happy_rate': 5, 'hunger_rate': 23}, session=session)
    >>> species_data
    <Species: testspecies>

    >>> species_data.save(session=session)
    >>> session.query(species.Species).all()
    [<Species: testspecies>]

    >>> owner_data, owner_errors = owner_schema.load({}, session=session)
    >>> owner_data
    <Owner: None []>

    >>> owner_data.user_id = user_data.id  # linking already existing user with its id
    >>> owner_data.save(session=session) # validating relationship
    >>> owner_data
    <Owner: <User: testuser> []>

    >>> owner_data, owner_errors2 = owner_schema.load({'pets': [{'name': 'testanimal', 'species_id': species_data.id}]}, instance=owner_data)
    >>> owner_data.save(session=session)
    >>> session.query(Owner).all()
    [<Owner: <User: testuser> [<Animal: testanimal>]>]

    >>> dump_data = owner_schema.dump(owner_data).data
    >>> import pprint  #ordering dict output
    >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
    {'id': 1,
     'pets': [{'name': 'testanimal', 'species': {'name': 'testspecies'}}],
     'user': {'email': 'tester@comp.any', 'id': 1, 'nick': 'testuser'}}

    >>> owner_schema.load(dump_data, session=session).data  # check invertibility
    <Owner: <User: testuser> [<Animal: testanimal>]>
    """


    class Meta:
        fields = ('id', 'user', 'pets', 'user_id')
        load_only = ('user_id',)
        dump_only = ('id', 'user')
        model = Owner

    #fields.Nested(UserSchema, only=["nick", "email"])
    pets = fields.Nested(AnimalSchema, many=True, load_only=["species_id"], dump_only=["species"])

    user = fields.Nested(UserSchema, dump_only=True)

    #pets = ma.HyperlinkRelated('animals')

    # links = ma.Hyperlinks({
    #     'self': ma.URLFor('book_detail', id='<id>'),
    #     'collection': ma.URLFor('book_list')
    # })
    #     model = Species
    #members = ma.HyperlinkRelated('members')


owner_schema = OwnerSchema()
#owners_schema = OwnerSchema(many=True)



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)