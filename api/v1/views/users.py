#!/usr/bin/python3
"""
User view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.user import User
from models import storage


@app_views.route("/users", strict_slashes=False)
@app_views.route("/users/<user_id>", strict_slashes=False)
def get_user(user_id=None):
    """
    GET METHOD
    """
    l_user = []
    if not user_id:
        for v in storage.all(User).values():
            l_user.append(v.to_dict())
        return jsonify(l_user)
    obj = storage.get(User, user_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id=None):
    """
    DELETE METHOD
    """
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """
    POST METHOD
    """
    try:
        obj_prop = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if obj_prop:
        if "email" not in obj_prop:
            abort(400, "Missing email")
        if "password" not in obj_prop:
            abort(400, "Missing password")
        obj = User(**obj_prop)
        obj.save()
        return (jsonify(obj.to_dict()), 201)
    abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id=None):
    """
    PUT METHOD
    """
    obj = storage.get(User, user_id)
    if user_id and obj:
        try:
            obj_prop = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if obj_prop:
            for k, v in obj_prop.items():
                if (
                    k is not "id"
                    and k is not "created_at"
		    and k is not "email"
                    and k is not "updated_at"
                ):
                    setattr(obj, k, v)
            obj.save()
            return (jsonify(obj.to_dict()))
        abort(400, "Not a JSON")
    abort(404)
