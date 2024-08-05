#!/usr/bin/python3
"""A file index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns json status"""
    json_resp = jsonify(status='OK')
    return json_resp


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    type_cls = {
           "amenities": storage.count('Amenity'),
           "cities": storage.count('City'),
           "places": storage.count('Place'),
           "reviews": storage.count('Review'),
           "states": storage.count('State'),
           "users": storage.count('User'),
    }

    return jsonify(type_cls)
