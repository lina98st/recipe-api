from flask import Blueprint, jsonify, abort, request
from ..models import Ingredient, db

bp = Blueprint("ingredients", __name__, url_prefix="/ingredients")


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    ingredients = Ingredient.query.all() # ORM performs SELECT query
    result = []
    for i in ingredients:
        result.append(i.serialize()) # build list of Ingredients as dictionaries
    return jsonify(result) # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    i = Ingredient.query.get_or_404(id)
    return jsonify(i.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain name
    if 'name' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    # construct Ingredients
    i = Ingredient(
        name=request.json['name'],
    )
    db.session.add(i) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(i.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    i = Ingredient.query.get_or_404(id)
    try:
        db.session.delete(i) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)



@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    i = Ingredient.query.get_or_404(id)

    if 'name' not in request.json:
        return abort(400)
    if 'name' in request.json:
        i.name = request.json['name']
    try:
        db.session.commit() # save UPDATE
        return jsonify(i.serialize())
    except:
        # something went wrong :(
        return jsonify(False)

