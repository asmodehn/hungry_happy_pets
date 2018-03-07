try:
    from ._bootstrap import ma
    from .models import Animal
    from .species import SpeciesSchema
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import ma
    from models import Animal
    from species import SpeciesSchema


from marshmallow import fields



class AnimalSchema(ma.ModelSchema):
    """This class represents the animals table.
        A Pet is part of a species and belongs to an owner

    Usage through marshmallow-sqlalchemy:
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:')
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import species, users, owners  #import other modules to resolve relationships
    >>> Animal.metadata.create_all(engine)

    >>> animal_data = Animal(name='testanimal', happy=4, hungry=42)
    >>> animal_data.species = species.Species(name='testspecies', happy_rate=0.5, hunger_rate=2.3)  # testing backref
    >>> test_owner = owners.Owner()
    >>> test_owner.user = users.User(nick='testuser', email='tester@comp.any')
    >>> animal_data.owner = test_owner

    >>> session.add(animal_data)
    >>> session.commit()
    >>> session.query(Animal).all()
    [<Animal: testanimal>]
    >>> session.query(owners.Owner).all()
    [<Owner: <User: testuser> [<Animal: testanimal>]>]

    >>> dump_data = animal_schema.dump(animal_data).data
    >>> import pprint  #ordering dict output
    >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
    {'happy': 4,
     'hungry': 42,
     'id': 1,
     'name': 'testanimal',
     'species': {'name': 'testspecies'}}

    >>> animal_schema.load(dump_data, session=session).data
    <Animal: testanimal>
    """

    class Meta:
        fields = ('id', 'name', 'happy', 'hungry', 'species')
        dump_only = ('id',)
        model = Animal

    species = fields.Nested(SpeciesSchema, only=["name"])
    #author = ma.HyperlinkRelated('owner')


animal_schema = AnimalSchema()
#animals_schema = UserSchema(many=True)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)