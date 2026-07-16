from flask import Blueprint, jsonify, abort, request
from ..models import User, db
import hashlib
import secrets
import datetime

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.route('', methods=['GET']) # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all() # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize()) # build list of Users as dictionaries
    return jsonify(result) # return JSON response


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id)
    return jsonify(u.serialize())


@bp.route('', methods=['POST'])
def create():
    # req body must contain email and password
    if 'email' not in request.json or 'password' not in request.json:
        return abort(400)
    # user with id of user_id must exist
    if len(request.json['password']) < 8:
        return abort(400)
    # construct User
    u = User(
        email=request.json['email'],
        created_at=datetime.date.today(),
        password_hash=scramble(request.json['password'])
     )
    db.session.add(u) # prepare CREATE statement
    db.session.commit() # execute CREATE statement
    return jsonify(u.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    u = User.query.get_or_404(id)
    try:
        db.session.delete(u) # prepare DELETE statement
        db.session.commit() # execute DELETE statement
        return jsonify(True)
    except:
        # something went wrong :(
        return jsonify(False)


@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    u = User.query.get_or_404(id)
    # user with id of user_id must exist
    if 'email' not in request.json and 'password' not in request.json:
        return abort(400)
    #check if email is valid
    if 'email' in request.json:
        if len(request.json['email']) < 3:
            return abort(400)
        u.email = request.json['email']
    #check if password length is correct
    if 'password' in request.json:
        if len(request.json['password']) < 8:
            return abort(400)
        u.password_hash = scramble(request.json['password'])

    try:
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)


