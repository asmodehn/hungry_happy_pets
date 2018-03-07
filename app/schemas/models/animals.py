try:
    from ._bootstrap import db
except SystemError:  # in case we call this module directly (doctest)
    from _bootstrap import db


from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType


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



if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)