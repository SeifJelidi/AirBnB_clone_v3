#!/usr/bin/python3
"""
State view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.state import State
from models import storage


@app_views.route("/states", strict_slashes=False)
@app_views.route("/states/<state_id>", strict_slashes=False)
def get_state(state_id=None):
    """
    GET METHOD
    """
    l_state = []
    if not state_id:
        for v in storage.all(State).values():
            l_state.append(v.to_dict())
        return jsonify(l_state)
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id=None):
    """
    DELETE METHOD
    """
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/states", methods=["POST"],
                 strict_slashes=False)
def post_state():
    """
    POST METHOD
    """
    try:
        obj_prop = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if obj_prop:
        if "name" in obj_prop:
            obj = State(**obj_prop)
            obj.save()
            return (jsonify(obj.to_dict()), 201)
        abort(400, "Missing name")
    abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=["PUT"],
                 strict_slashes=False)
def put_state(state_id=None):
    """
    PUT METHOD
    """
    obj = storage.get(State, state_id)
    if state_id and obj:
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
