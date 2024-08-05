#!/usr/bin/python3
"""A view for User objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def retrieve_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User).values()
    userList = []
    for user in users:
        userList.append(user.to_dict())
    return jsonify(userList)


@app_views.route('/users/<user_id>', strict_slashes=False)
def retrieve_userobj(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        abort(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def removes_userobj(user_id):
    """Deletes a User object"""
    User = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def make_user():
    """Creates a User"""
    user_req = request.get_json()

    if not user_req:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in user_req:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in user_req:
        return jsonify({"error": "Missing password"}), 400

    user_new = User(**user_req)
    user_new.save()
    return jsonify(user_new.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Updates a User object"""
    user = storage.get(User, user_id)
    user_req = request.get_json()

    if user is None:
        abort(404)
    if not user_req:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in user_req.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200
