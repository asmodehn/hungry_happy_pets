try:
    from ._bootstrap import ma
    from .models import Species
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import ma
    from models import Species


import http

from marshmallow import post_load

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify, request


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


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
