#!/usr/bin/python3
"""A view for Review objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import jsonify
from flask import abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def retrieve_review(place_id):
    """Retrieves the list of all Review objects of a state"""
    place = storage.get(Place, place_id)
    reviewList = []
    if not place:
        abort(404)
    for review in place.reviews:
        reviewList.append(review.to_dict())
    return jsonify(reviewList)


@app_views.route('reviews/<review_id>', strict_slashes=False)
def retrieve_rvobj(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def removes_rvobj(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def make_review(place_id):
    """Creates a Review"""
    review_req = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not review_req:
        return jsonify({"error": "Not a JSON"}), 400
    if "user_id" not in review_req:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, review_req['user_id'])
    if not user:
        abort(404)

    if "text" not in review_req:
        return jsonify({"error": "Missing text"}), 400

    review_req["place_id"] = place_id
    review_new = Review(**review_req)
    review_new.save()
    return jsonify(review_new.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Place object"""
    review = storage.get(Review, review_id)
    review_req = request.get_json()

    if review is None:
        abort(404)
    if not review_req:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in review_req.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    review.save()
    return jsonify(review.to_dict()), 200
