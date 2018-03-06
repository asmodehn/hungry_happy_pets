try:
    from .addons import db, ma
except SystemError:  # in case we call this module directly (doctest)
    from addons import db, ma


from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify



class Animal(db.Model):
    """This class represents the animals table.
    A Pet is part of a species and belongs to an owner

    Usage through sqlalchemy :
    >>> import sqlalchemy
    >>> engine = sqlalchemy.create_engine('sqlite:///:memory:')
    >>> Session = sqlalchemy.orm.sessionmaker(bind=engine)
    >>> session = Session()

    >>> import species, users, owners  #import other modules to resolve relationships
    >>> Animal.metadata.create_all(engine)

    >>> animal_data = Animal(name='testanimal', happy=4, hungry=42)
    >>> animal_data.species = species.Species(name='testspecies', happy_rate=0.5, hunger_rate=2.3)
    >>> test_owner = owners.Owner()
    >>> test_owner.user = users.User(nick='testuser', email='tester@comp.any')
    >>> animal_data.owner = test_owner

    >>> session.add(animal_data)
    >>> session.commit()
    >>> session.query(Animal).all()
    [<Animal: testanimal>]
    >>> session.query(owners.Owner).all()
    [<Owner: <User: testuser> [<Animal: testanimal>]>]
    """

    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    happy = db.Column(db.Integer())
    hungry = db.Column(db.Integer())
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=False)
    species_id = db.Column(db.Integer, db.ForeignKey('species.id'), nullable=False)

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
    def get_all():
        return Animal.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Animal: {}>".format(self.name)



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
    >>> animal_data.species = species.Species(name='testspecies', happy_rate=0.5, hunger_rate=2.3)
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
    {'date_created': '...',
     'date_modified': '...',
     'happy': 4,
     'hungry': 42,
     'id': 1,
     'name': 'testanimal'}

    >>> animal_schema.load(dump_data, session=session).data
    <Animal: testanimal>
    """

    class Meta:
        model = Animal
    #author = ma.HyperlinkRelated('owner')


animal_schema = AnimalSchema()
#animals_schema = UserSchema(many=True)


def animals():
    all_animals = Animal.all()
    result = animal_schema.dump(all_animals, many=True)
    return jsonify(result.data)


def animals_detail(id):
    animal = Animal.query.get(id)
    return animal_schema.jsonify(animal)
# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/authors/42",
#         "collection": "/api/authors/"
#     }
# }


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)