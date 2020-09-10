#!/usr/bin/python3
"""
Handling routes
"""

from api.v1.views import app_views
from models import storage
from flask import jsonify


@app_views.route("/status")
def status_ok():
    """
    Return the status of the API:
    """
    return jsonify(status="OK")


@app_views.route("/stats")
def stats_count():
    """
    retrieves the number of each objects by type
    """
    types = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
        }
    dict_count = {}
    for k, t in types.items():
        dict_count[t] = storage.count(k)
    return jsonify(dict_count)
