from flask import Blueprint, jsonify, abort, request
from ..models import Recipe, Category, db

bp = Blueprint("recipes", __name__, url_prefix="/recipes")


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    recipes = Recipe.query.all() # ORM performs SELECT query
    result = []
    for r in recipes:
        result.append(r.serialize()) # build list of Recipe as dictionaries
    return jsonify(result) # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    r = Recipe.query.get_or_404(id)
    return jsonify(r.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain category_id and title
    if 'category_id' not in request.json or 'title' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    Category.query.get_or_404(request.json['category_id'])
    # construct Recipe
    r = Recipe(
        title=request.json['title'],
        instructions=request.json['instructions'],
        cooking_time=request.json['cooking_time'],
        category_id=request.json['category_id']
    )
    db.session.add(r) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(r.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    r = Recipe.query.get_or_404(id)
    try:
        db.session.delete(r) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)



@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    r = Recipe.query.get_or_404(id)

    if 'title' not in request.json and \
   'instructions' not in request.json and \
   'cooking_time' not in request.json and \
   'category_id' not in request.json:
        return abort(400)
    if 'title' in request.json:
        r.title = request.json['title']
    if 'instructions' in request.json:
        r.instructions = request.json['instructions']
    if 'cooking_time' in request.json:
        r.cooking_time = request.json['cooking_time']
    if 'category_id' in request.json:
        Category.query.get_or_404(request.json['category_id'])
        r.category_id = request.json['category_id']
    try:
        db.session.commit() # save UPDATE
        return jsonify(r.serialize())
    except:
        # something went wrong :(
        return jsonify(False)

