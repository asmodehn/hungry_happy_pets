import http

try:
    from .schemas import models, user_schema
except SystemError:  # in case we call this module directly (doctest)
    from schemas import models, user_schema

from sqlalchemy_utils import PasswordType, EmailType, UUIDType  #,NumericRangeType
from flask import jsonify, request
from marshmallow import post_load


def users():
    all_users = models.User.all()
    user_dict, errors = user_schema.dump(all_users, many=True)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def user_read(id):
    user = models.User.query.get(id)
    if not user:
        return '', http.HTTPStatus.NOT_FOUND
    user_dict, errors = user_schema.dump(user)
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


def user_edit(id):
    data = request.get_json()
    user = models.User.query.get(id)

    if not user:
        return '', http.HTTPStatus.NOT_FOUND

    for k, v in data.items():
        setattr(user, k, v)

    user_dict, errors = user_schema.dump(user)
    if not errors:
        return user_dict
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def user_add():
    data = request.get_json()
    user, errors = user_schema.load(data, )
    if not errors:
        user.save()

    user_dict, errors = user_schema.dump(user)
    if not errors:
        return user_dict, http.HTTPStatus.CREATED
    else:  # break properly
        return '', http.HTTPStatus.INTERNAL_SERVER_ERROR


def user_delete(id):
    user = models.User.query.get(id)
    if user:
        user.delete()
        return '', http.HTTPStatus.NO_CONTENT
    else:
        return '', http.HTTPStatus.NOT_FOUND

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)


