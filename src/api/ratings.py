from flask import Blueprint, jsonify, abort, request
from ..models import Rating, User, Recipe, db
import datetime

bp = Blueprint("ratings", __name__, url_prefix="/ratings")


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    ratings = Rating.query.all() # ORM performs SELECT query
    result = []
    for ra in ratings:
        result.append(ra.serialize()) # build list of Ratings as dictionaries
    return jsonify(result) # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    ra = Rating.query.get_or_404(id)
    return jsonify(ra.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain score, created_at, recipe_id and user_id
    if (
        'score' not in request.json
         or 'created_at' not in request.json
         or 'recipe_id' not in request.json
         or 'user_id' not in request.json
    ):
         return abort(400)
    # recipe and user must exist
    Recipe.query.get_or_404(request.json['recipe_id'])
    User.query.get_or_404(request.json['user_id'])
    # construct Rating
    ra = Rating(
        score=request.json['score'],
        created_at=datetime.date.fromisoformat(request.json['created_at']),
        recipe_id=request.json['recipe_id'],
        user_id=request.json['user_id']
    )
    db.session.add(ra) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(ra.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    ra = Rating.query.get_or_404(id)
    try:
        db.session.delete(ra) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)



@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    ra = Rating.query.get_or_404(id)

    if 'score' not in request.json and \
   'created_at' not in request.json and \
   'recipe_id' not in request.json and \
   'user_id' not in request.json:
        return abort(400)
    if 'score' in request.json:
        ra.score = request.json['score']
    if 'created_at' in request.json:
        ra.created_at = datetime.date.fromisoformat(request.json['created_at'])
    if 'recipe_id' in request.json:
        Recipe.query.get_or_404(request.json['recipe_id'])
        ra.recipe_id = request.json['recipe_id']
    if 'user_id' in request.json:
        User.query.get_or_404(request.json['user_id'])
        ra.user_id = request.json['user_id']
    try:
        db.session.commit() # save UPDATE
        return jsonify(ra.serialize())
    except:
        # something went wrong :(
        return jsonify(False)

