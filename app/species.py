try:
    from .schemas import models, species_schema
except SystemError:  # in case we call this module directly (doctest)
    from schemas import models, species_schema


import http

from marshmallow import post_load

from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify, request



def species():
    """
    Retrieves all species
    :return:
    """
    all_species = models.Species.all()
    user_dict, errors = species_schema.dump(all_species, many=True)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def species_read(id):
    """
    Retrieve a species
    :param id: the species id
    :return:
    """
    species = models.Species.query.get(id)
    if not species:
        return '', http.HTTPStatus.NOT_FOUND
    species_dict, errors = species_schema.dump(species)
    if not errors:
        return species_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/authors/42",
#         "collection": "/api/authors/"
#     }
# }


def species_edit(id):
    """
    Edit a species data
    :param id:
    :return:
    """
    data = request.get_json()
    user = models.Species.query.get(id)

    if not user:
        return '', http.HTTPStatus.NOT_FOUND

    for k, v in data.items():
        setattr(user, k, v)

    species_dict, errors = species_schema.dump(user)
    if not errors:
        return species_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def species_add():
    """
    Adds a species
    :return:
    """
    data = request.get_json()
    user, errors = species_schema.load(data, )
    if not errors:
        user.save()

    user_dict, errors = species_schema.dump(user)
    if not errors:
        return user_dict, http.HTTPStatus.CREATED
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def species_delete(id):
    """
    Deletes a species
    :param id:
    :return:
    """
    species = models.Species.query.get(id)
    if species:
        species.delete()
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
