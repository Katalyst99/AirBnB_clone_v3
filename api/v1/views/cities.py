#!/usr/bin/python3
"""A view for City objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def retrieve_cities(state_id):
    """Retrieves the list of all City objects of a state"""
    state = storage.get(State, state_id)
    cityList = []
    if not state:
        abort(404)
    for city in state.cities:
        cityList.append(city.to_dict())
    return jsonify(cityList)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def retrieve_cityobj(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def removes_cityobj(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def make_city(state_id):
    """Creates a City"""
    city_req = request.get_json()
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    if not city_req:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in city_req:
        return jsonify({"error": "Missing name"}), 400

    city_req["state_id"] = state_id
    city_new = City(**city_req)
    city_new.save()
    return jsonify(city_new.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    city_req = request.get_json()

    if city is None:
        abort(404)
    if not city_req:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in city_req.items():
        if k not in ['id', 'state_id' 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200
