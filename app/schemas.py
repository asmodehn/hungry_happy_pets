
from flask_marshmallow import Marshmallow

from . import models


# initialize marshmallow
ma = Marshmallow()


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('email', 'date_created', '_links')
        # Smart hyperlinking
        _links = ma.Hyperlinks({
            'self': ma.URLFor('author_detail', id='<id>'),
            'collection': ma.URLFor('authors')
        })


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class OwnerSchema(ma.ModelSchema):
    class Meta:
        model = models.Owner
    animals = ma.HyperlinkRelated('animals')


owner_schema = OwnerSchema()
owners_schema = OwnerSchema(many=True)


class RaceSchema(ma.ModelSchema):
    class Meta:
        model = models.Race
    animals = ma.HyperlinkRelated('animals')


race_schema = UserSchema()
races_schema = UserSchema(many=True)


class AnimalSchema(ma.Schema):
    class Meta:
        model = models.Animal
    author = ma.HyperlinkRelated('owner')


animal_schema = UserSchema()
animals_schema = UserSchema(many=True)
