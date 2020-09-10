#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id=None):
    """
    GET METHOD
    """
    l_amenity = []
    if not amenity_id:
        for v in storage.all(Amenity).values():
            l_amenity.append(v.to_dict())
        return jsonify(l_amenity)
    obj = storage.get(Amenity, amenity_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    DELETE METHOD
    """
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """
    POST METHOD
    """
    try:
        obj_prop = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if obj_prop:
        if "name" in obj_prop:
            obj = Amenity(**obj_prop)
            obj.save()
            return (jsonify(obj.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id=None):
    """
    PUT METHOD
    """
    obj = storage.get(Amenity, amenity_id)
    if amenity_id and obj:
        try:
            obj_prop = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if obj_prop:
            for k, v in obj_prop.items():
                if (
                    k is not "id"
                    and k is not "created_at"
                    and k is not "updated_at"
                ):
                    setattr(obj, k, v)
            obj.save()
            return (jsonify(obj.to_dict()))
        abort(400, "Not a JSON")
    abort(404)
