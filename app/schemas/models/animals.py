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

    >>> spec = species.Species(name='testspecies', happy_rate=0.5, hunger_rate=2.3)
    >>> spec.save(session=session)
    >>> session.query(species.Species).all()
    [<Species: testspecies>]

    >>> animal_data = Animal(name='testanimal', happy=4, hungry=42, species_id=spec.id)
    >>> animal_data
    <Animal: testanimal>

    >>> test_owner = owners.Owner()
    >>> test_owner.user = users.User(nick='testuser', email='tester@comp.any')
    >>> test_owner.save(session=session)  # need to commit to get id assigned

    >>> animal_data.owner_id = test_owner.id
    >>> animal_data.save(session=session)

    >>> session.query(Animal).all()
    [<Animal: testanimal>]

    >>> session.query(owners.Owner).all()
    [<Owner: <User: testuser> [<Animal: testanimal>]>]
    """

    __tablename__ = 'animals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    happy = db.Column(db.Integer(), default=0)
    hungry = db.Column(db.Integer(), default=0)
    owner_id = db.Column(db.Integer, db.ForeignKey('owners.id'), nullable=True)  # allow orphan pets
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

    def save(self, session=None, commit=True):
        if session is None:
            session = db.session
        session.add(self)
        if commit:
            self.commit(session=session)

    @staticmethod
    def all():
        return Animal.query.all()

    def delete(self, session=None, commit=True):
        if session is None:
            session = db.session
        session.delete(self)
        if commit:
            self.commit(session=session)

    def commit(self, session=None):
        if session is None:
            session = db.session
        try:
            session.commit()
        except:
            session.rollback()
            raise

    def __repr__(self):
        return "<Animal: {} {} {}>".format(self.name, self.species, self.owner)


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
