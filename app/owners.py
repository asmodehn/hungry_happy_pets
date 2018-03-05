from .addons import db, ma

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify



class Owner(db.Model):
    """This class represents the owners table.
    Owner is needed to differentiate the user data (generic & widely used), with the owner data (specific to our app)
    """

    __tablename__ = 'owners'

    id = db.Column(db.Integer, primary_key=True)
    #uuid = db.Column(UUIDType(binary=False))  # http://docs.sqlalchemy.org/en/rel_0_9/core/custom_types.html?highlight=guid#backend-agnostic-guid-type
    name = db.Column(db.String)


    # authoring
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, nick, email):
        """initialize with name."""
        self.nick = nick
        self.email = email

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Owner: {}>".format(self.name)


class OwnerSchema(ma.ModelSchema):
    class Meta:
        model = Owner

    animals = ma.HyperlinkRelated('animals')

owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)


def owners():
    all_owners = Owner.all()
    result = owner_schema.dump(all_owners, many=True)
    return jsonify(result.data)
    # OR
    # return owner_schema.jsonify(all_users)


def owner_detail(id):
    owner = Owner.query.get(id)
    return owner_schema.jsonify(owner)
# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/authors/42",
#         "collection": "/api/authors/"
#     }
# }
