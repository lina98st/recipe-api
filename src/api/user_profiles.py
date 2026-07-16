from flask import Blueprint, jsonify, abort, request
from ..models import UserProfile, User, db

bp = Blueprint("user_profiles", __name__, url_prefix="/user_profiles")


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    user_profile = UserProfile.query.all() # ORM performs SELECT query
    result = []
    for up in user_profile:
        result.append(up.serialize()) # build list of Recipe as dictionaries
    return jsonify(result) # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    up = UserProfile.query.get_or_404(id)
    return jsonify(up.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain category_id and title
    if 'display_name' not in request.json or 'user_id' not in request.json or 'avatar_url' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    User.query.get_or_404(request.json['user_id'])
    # construct UserProfile
    up = UserProfile(
        display_name=request.json['display_name'],
        bio=request.json['bio'],
        user_id=request.json['user_id'],
        avatar_url=request.json['avatar_url']
    )
    db.session.add(up) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(up.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    up = UserProfile.query.get_or_404(id)
    try:
        db.session.delete(up) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)



@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    up = UserProfile.query.get_or_404(id)

    if 'display_name' not in request.json and \
   'bio' not in request.json and \
   'user_id' not in request.json and \
   'avatar_url' not in request.json:
        return abort(400)
    if 'display_name' in request.json:
        up.display_name = request.json['display_name']
    if 'bio' in request.json:
        up.bio = request.json['bio']
    if 'user_id' in request.json:
        User.query.get_or_404(request.json['user_id'])
        up.user_id = request.json['user_id']
    if 'avatar_url' in request.json:
        up.avatar_url = request.json['avatar_url']
    try:
        db.session.commit() # save UPDATE
        return jsonify(up.serialize())
    except:
        # something went wrong :(
        return jsonify(False)

