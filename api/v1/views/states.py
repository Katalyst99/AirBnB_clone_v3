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
    st = storage.get('State', state_id)
    if st:
        st = st.to_dict()
        return jsonify(st), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def removes_stateobj(state_id):
    """Deletes a State object"""
    st = storage.get('State', state_id)
    Dict = {}
    if st:
        storage.delete(st)
        storage.save()
        return jsonify(Dict), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def make_state():
    """Creates a State"""
    user_req = request.get_json()

    if not user_req:
        message = jsonify('Not a JSON'), 400
        return message
    if "name" not in user_req:
        message2 = jsonify('Missing name'), 400
        return message2

    state_new = State(**user_req)
    state_new.save()
    return jsonify(state_new.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    user_req = request.get_json()
    st = storage.get('State', state_id)

    if not st:
        abort(404)
    if not user_req:
        mes = jsonify('Not a JSON'), 400
        return mes

    for k, v in user_req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(st, k, v)
    st.save()
    return jsonify(st.to_dict()), 200
