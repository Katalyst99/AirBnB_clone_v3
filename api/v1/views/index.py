#!/usr/bin/python3
"""A file index.py"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns json status"""
    json_resp = jsonify(status='OK')
    return json_resp
