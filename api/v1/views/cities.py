#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.state import State
from models import storage


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_city_by_state(state_id=None):
    """
    GET METHOD (list of all City objects of a State)
    """
    l_city = []
    obj = storage.get(State, state_id)
    if obj:
        for c in obj.cities:
            l_city.append(v.to_dict())
        return jsonify(l_city)
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id=None):
    """GET METHOD"""
    obj = storage.get(City, city_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id=None):
    """
    DELETE METHOD
    """
    obj = storage.get(City, city_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """
    POST METHOD
    """
    verif_state = storage.get(State, state_id)
    if not verif_state:
        abort(404)
    try:
        obj_prop = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if obj_prop:
        if "name" in obj_prop:
            obj = City(**obj_prop)
            setattr(obj, "state_id", state_id)
            obj.save()
            return (jsonify(obj.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id=None):
    """
    PUT METHOD
    """
    obj = storage.get(City, city_id)
    if city_id and obj:
        try:
            obj_prop = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if obj_prop:
            for k, v in obj_prop.items():
                if (
                    k is not "id"
                    and k is not "state_id"
                    and k is not "created_at"
                    and k is not "updated_at"
                ):
                    setattr(obj, k, v)
            obj.save()
            return (jsonify(obj.to_dict()))
        abort(400, "Not a JSON")
    abort(404)
