#!/usr/bin/python3
"""
Handling routes
"""

from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def status_ok():
    """
    Return the status of the API:
    """
    return jsonify(status="OK")
