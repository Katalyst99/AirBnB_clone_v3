#!/usr/bin/python3
"""A view for Place objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def retrieve_place(city_id):
    """Retrieves the list of all Place objects of a state"""
    city = storage.get(City, city_id)
    placeList = []
    if not city:
        abort(404)
    for place in city.places:
        cityList.append(place.to_dict())
    return jsonify(placeList)


@app_views.route('/places/<place_id>', strict_slashes=False)
def retrieve_placeobj(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def removes_placeobj(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def make_place(city_id):
    """Creates a Place"""
    place_req = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    if not place_req:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in place_req:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, place_req['user_id'])
    if user is None:
        abort(404)

    if "name" not in place_req:
        return jsonify({"error": "Missing name"}), 400

    place_req["city_id"] = city_id
    place_new = Place(**place_req)
    place_new.save()
    return jsonify(place_new.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    place_req = request.get_json()

    if place is None:
        abort(404)
    if not place_req:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in place_req.items():
        if k not in ['id', 'user_id', 'state_id', 'created_at', 'updated_at']:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200
