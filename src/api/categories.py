from flask import Blueprint, jsonify, abort, request
from ..models import Category, db

bp = Blueprint("categories", __name__, url_prefix="/categories")


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    categories = Category.query.all() # ORM performs SELECT query
    result = []
    for c in categories:
        result.append(c.serialize()) # build list of Categories as dictionaries
    return jsonify(result) # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    c = Category.query.get_or_404(id)
    return jsonify(c.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain name
    if 'name' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    # construct Category
    c = Category(
        name=request.json['name'],
    )
    db.session.add(c) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(c.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    c = Category.query.get_or_404(id)
    try:
        db.session.delete(c) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)



@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    c = Category.query.get_or_404(id)

    if 'name' not in request.json:
        return abort(400)
    if 'name' in request.json:
        c.name = request.json['name']
    try:
        db.session.commit() # save UPDATE
        return jsonify(c.serialize())
    except:
        # something went wrong :(
        return jsonify(False)

