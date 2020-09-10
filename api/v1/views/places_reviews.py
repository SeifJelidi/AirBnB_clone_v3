#!/usr/bin/python3
"""
Review view
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_review_by_place(place_id=None):
    """
    GET METHOD (list of all Review objects of a Place)
    """
    l_review = []
    obj = storage.get(Place, place_id)
    if obj:
        for v in obj.reviews:
            l_review.append(v.to_dict())
        return jsonify(l_review)
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id=None):
    """
    GET METHOD
    """
    obj = storage.get(Review, review_id)
    if obj:
        return jsonify(obj.to_dict())
    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """
    DELETE METHOD
    """
    obj = storage.get(Review, review_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({})
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """
    POST METHOD
    """
    verif_place = storage.get(Place, place_id)
    if not verif_place:
        abort(404)
    try:
        obj_prop = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if obj_prop:
        if "user_id" not in obj_prop:
            abort(400, "Missing user_id")
        if storage.get(User, obj_prop["user_id"]) is None:
            abort(404)
        if "text" not in obj_prop:
            abort(400, "Missing text")
        obj = Review(**obj_prop)
        setattr(obj, "place_id", place_id)
        obj.save()
        return (jsonify(obj.to_dict()), 201)
    abort(400, "Not a JSON")


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id=None):
    """
    PUT METHOD
    """
    obj = storage.get(Review, review_id)
    if obj:
        try:
            obj_prop = request.get_json()
        except Exception:
            abort(400, "Not a JSON")
        if obj_prop:
            for k, v in obj_prop.items():
                if (
                    k is not "id"
                    and k is not "place_id"
                    and k is not "user_id"
                    and k is not "created_at"
                    and k is not "updated_at"
                ):
                    setattr(obj, k, v)
            obj.save()
            return (jsonify(obj.to_dict()))
        abort(400, "Not a JSON")
    abort(404)
