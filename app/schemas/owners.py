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

    >>> owner_data = Owner()
    >>> owner_data.user = users.User(nick='testuser', email='tester@comp.any')

    >>> animal_data = models.Animal(name='testanimal', happy=4, hungry=42)
    >>> animal_data.species = models.Species(name='testspecies', happy_rate=0.5, hunger_rate=2.3)
    >>> owner_data.pets = [animal_data]

    >>> session.add(owner_data)
    >>> session.commit()
    >>> session.query(Owner).all()
    [<Owner: <User: testuser> [<Animal: testanimal>]>]

    >>> dump_data = owner_schema.dump(owner_data).data
    >>> import pprint  #ordering dict output
    >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
    {'id': 1,
     'pets': [{'name': 'testanimal', 'species': {'name': 'testspecies'}}],
     'user': {'email': 'tester@comp.any', 'id': 1, 'nick': 'testuser'}}

    >>> owner_schema.load(dump_data, session=session).data
    <Owner: <User: testuser> [<Animal: testanimal>]>
    """


    class Meta:
        fields = ('id', 'user', 'pets')
        # dump_only = ('id',)
        model = Owner

    #fields.Nested(UserSchema, only=["nick", "email"])
    pets = fields.Nested(AnimalSchema, many=True, only=["name", "species"])

    user = fields.Nested(UserSchema, exclude=('author',))

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