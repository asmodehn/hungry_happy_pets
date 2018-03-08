try:
    from ._bootstrap import ma
    from .models import Animal, Species
    from .species import SpeciesSchema
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import ma
    from models import Animal, Species
    from species import SpeciesSchema


from marshmallow import fields, pre_load


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

    >>> species_data, species_errors = species.species_schema.load({'name':'testspecies', 'happy_rate': 0.5, 'hunger_rate': 2.3}, session=session)
    >>> species_data
    <Species: testspecies>

    >>> species_data.save(session=session)
    >>> session.query(species.Species).all()
    [<Species: testspecies>]

    >>> animal_data = Animal(name='testanimal', happy=4, hungry=42)
    >>> animal_data.species_id = species_data.id

    >>> user_data, user_errors = users.user_schema.load({'nick': 'testuser', 'email': 'tester@comp.any'}, session=session)
    >>> user_data
    <User: testuser>

    >>> user_data.save(session=session)
    >>> session.query(users.User).all()
    [<User: testuser>]

    >>> owner_data, owner_errors = owners.owner_schema.load({}, session=session)
    >>> owner_data
    <Owner: None []>

    >>> owner_data.user_id = user_data.id  # linking already existing user with its id
    >>> owner_data.save(session=session) # validating relationship
    >>> owner_data
    <Owner: <User: testuser> []>

    >>> animal_data.owner_id = owner_data.id
    >>> animal_data.save(session=session)
    >>> session.query(Animal).all()
    [<Animal: testanimal <Species: testspecies>>]
    >>> session.query(owners.Owner).all()
    [<Owner: <User: testuser> [<Animal: testanimal <Species: testspecies>>]>]

    >>> dump_data = animal_schema.dump(animal_data).data
    >>> import pprint  #ordering dict output
    >>> pprint.pprint(dump_data)  # doctest: +ELLIPSIS
    {'happy': 4,
     'hungry': 42,
     'id': 1,
     'name': 'testanimal',
     'species': {'name': 'testspecies'}}

    >>> animal_schema.load(dump_data, session=session).data
    <Animal: testanimal <Species: testspecies>>
    """

    class Meta:
        fields = ('id', 'name', 'happy', 'hungry', 'species', 'species_id', 'owner', 'owner_id')
        load_only = ('species_id', 'owner_id')
        dump_only = ('id', 'species', 'owner')
        model = Animal

    species = fields.Nested(SpeciesSchema, dump_only=True)
    # indirect nested relation to avoid cycle
    owner = fields.Nested('OwnerSchema', dump_only=True, exclude=('pets', ))
    #author = ma.HyperlinkRelated('owner')

    # @pre_load
    # def match_species_by_unique_name(self, data):
    #     if 'species' in data:
    #         species = data.pop('species')
    #         matched = self.model.session.query(Species).filter_by(name = species.get('name')).one()
    #
    #         if matched:
    #             data.setdefault('species_id', matched.id)
    #         else:
    #             raise RuntimeError
    #
    #     return data



animal_schema = AnimalSchema()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)