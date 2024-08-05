#!/usr/bin/python3
"""A view for State objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def retrieve_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenityList = []
    for amenity in amenities:
        amenityList.append(amenity.to_dict())
    return jsonify(amenityList)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def retrieve_amenityobj(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def removes_amenityobj(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def make_amenity():
    """Creates a Amenity"""
    amenity_req = request.get_json()

    if not amenity_req:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in amenity_req:
        return jsonify({"error": "Missing name"}), 400

    amenity_new = Amenity(**amenity_req)
    amenity_new.save()
    return jsonify(amenity_new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    amenity_req = request.get_json()

    if amenity is None:
        abort(404)
    if not amenity_req:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in user_req.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
