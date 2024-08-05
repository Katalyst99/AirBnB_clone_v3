#!/usr/bin/python3
"""A view for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def retrieve_states():
    """Retrieves the list of all State objects"""
    states = storage.all(State).values()
    stateList = []
    for st in states:
        stateList.append(st.to_dict())
    return jsonify(stateList)


@app_views.route('/states/<state_id>', strict_slashes=False)
def retrieve_stateobj(state_id):
    """Retrieves a State object"""
    st = storage.get(State, state_id)
    if st:
        return jsonify(st.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def removes_stateobj(state_id):
    """Deletes a State object"""
    st = storage.get(State, state_id)
    if st:
        storage.delete(st)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def make_state():
    """Creates a State"""
    user_req = request.get_json()

    if not user_req:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in user_req:
        return jsonify({"error": "Missing name"}), 400

    state_new = State(**user_req)
    state_new.save()
    return jsonify(state_new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    st = storage.get(State, state_id)
    user_req = request.get_json()

    if st is None:
        abort(404)
    if not user_req:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in user_req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(st, k, v)
    st.save()
    return jsonify(st.to_dict()), 200
