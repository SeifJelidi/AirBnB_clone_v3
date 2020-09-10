#!/usr/bin/python3
"""
City view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_place_by_city(city_id=None):
    """
    GET METHOD (list of all Place objects of a City)
    """
    l_place = []
    obj = storage.get(City, city_id)
    if obj:
        for v in obj.places:
            l_place.append(v.to_dict())
        return jsonify(l_place)
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id=None):
    """GET METHOD"""
    obj = storage.get(Place, place_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id=None):
    """
    DELETE METHOD
    """
    obj = storage.get(Place, place_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
    POST METHOD
    """
    verif_city = storage.get(City, city_id)
    if not verif_city:
        abort(404)
    try:
        obj_prop = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if obj_prop:
        if "user_id" not in obj_prop:
            abort(400, "Missing user_id")
        if storage.get(User, obj_prop["user_id"]) is None:
            abort(400)
        if "name" not in obj_prop:
            abort(400, "Missing name")
        obj = Place(**obj_prop)
        setattr(obj, "city_id", city_id)
        obj.save()
        return (jsonify(obj.to_dict()), 201)
    abort(400, "Not a JSON")


@app_views.route("/cities/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id=None):
    """
    PUT METHOD
    """
    obj = storage.get(Place, place_id)
    if place_id and obj:
        try:
            obj_prop = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if obj_prop:
            for k, v in obj_prop.items():
                if (
                    k is not "id"
                    and k is not "city_id"
                    and k is not "user_id"
                    and k is not "created_at"
                    and k is not "updated_at"
                ):
                    setattr(obj, k, v)
            obj.save()
            return (jsonify(obj.to_dict()))
        abort(400, "Not a JSON")
    abort(404)
