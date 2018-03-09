import http

try:
    from .schemas import models, animal_schema
except SystemError:  # in case we call this module directly (doctest)
    from schemas import models, animal_schema

from flask import jsonify, request



def animals():
    """
    Retrieves all animals
    :return:
    """
    all_animals = models.Animal.all()
    animal_dict, errors = animal_schema.dump(all_animals, many=True)
    if not errors:
        return animal_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def animal_read(id):
    """
    Retrieve an animal
    :param id:
    :return:
    """
    animal = models.Animal.query.get(id)
    if not animal:
        return '', http.HTTPStatus.NOT_FOUND
    animal_dict, errors = animal_schema.dump(animal)
    if not errors:
        return animal_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def animal_edit(id):
    """
    Edit an animal data
    :param id: the animal id
    :return:
    """
    data = request.get_json()
    animal = models.Animal.query.get(id)

    if not animal:
        return '', http.HTTPStatus.NOT_FOUND

    for k, v in data.items():
        setattr(animal, k, v)

    user_dict, errors = animal_schema.dump(animal)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def animal_add():
    """
    Adds an animal
    :return:
    """
    data = request.get_json()
    animal, errors = animal_schema.load(data, )
    if not errors:
        animal.save()

    animal_dict, errors = animal_schema.dump(animal)
    if not errors:
        return animal_dict, http.HTTPStatus.CREATED
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def animal_delete(id):
    """
    Deletes an owner
    :param id: the owner id
    :return:
    """
    animal = models.Animal.query.get(id)
    if animal:
        animal.delete()
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)