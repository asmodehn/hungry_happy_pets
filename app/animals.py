try:
    from .schemas import models, animal_schema
except SystemError:  # in case we call this module directly (doctest)
    from schemas import models, animal_schema


from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify
from marshmallow import fields



def animals():
    all_animals = models.Animal.all()
    result = animal_schema.dump(all_animals, many=True)
    return jsonify(result.data)


def animals_detail(id):
    animal = models.Animal.query.get(id)
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