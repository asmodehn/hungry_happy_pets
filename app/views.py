from flask import jsonify

from .models import User
from .schemas import user_schema, users_schema


def users():
    all_users = User.all()
    result = users_schema.dump(all_users)
    return jsonify(result.data)
    # OR
    # return user_schema.jsonify(all_users)


def user_detail(id):
    user = User.get(id)
    return user_schema.jsonify(user)
# {
#     "email": "fred@queen.com",
#     "date_created": "Fri, 25 Apr 2014 06:02:56 -0000",
#     "_links": {
#         "self": "/api/authors/42",
#         "collection": "/api/authors/"
#     }
# }

