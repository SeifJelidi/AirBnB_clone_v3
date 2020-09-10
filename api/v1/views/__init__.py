#!/usr/bin/python3
"""
init module
"""

from flask import Blueprint
from api.v1.views.index import *
from api.v1.views.states import *

app_views = Blueprint("app_views", __name__)
