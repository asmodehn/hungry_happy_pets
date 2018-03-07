try:
    from .schemas import models, owner_schema
except SystemError:  # in case we call this module directly (doctest)
    from schemas import models, owner_schema

import http
from sqlalchemy_utils import PasswordType, EmailType, UUIDType, ColorType  #,NumericRangeType
from flask import jsonify, request
from marshmallow import fields, post_load



def owners():
    all_users = models.Owner.get_all()
    user_dict, errors = owner_schema.dump(all_users, many=True)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def owner_read(id):
    user = models.Owner.query.get(id)
    if not user:
        return '', http.HTTPStatus.NOT_FOUND
    user_dict, errors = owner_schema.dump(user)
    if not errors:
        return user_dict
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


def owner_edit(id):
    data = request.get_json()
    owner = models.Owner.query.get(id)

    if not owner:
        return '', http.HTTPStatus.NOT_FOUND

    for k, v in data.items():
        setattr(owner, k, v)

    user_dict, errors = owner_schema.dump(owner)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def owner_add():
    data = request.get_json()
    owner, errors = owner_schema.load(data, )
    if not errors:
        owner.save()

    owner_dict, errors = owner_schema.dump(owner)
    if not errors:
        return owner_dict, http.HTTPStatus.CREATED
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def owner_delete(id):
    owner = models.Owner.query.get(id)
    if owner:
        owner.delete()
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.NOT_FOUND


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)