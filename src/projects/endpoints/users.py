from datetime import datetime
import jwt
from functools import wraps
from flask import request, jsonify, Blueprint, current_app
from projects import db, bcrypt
from projects.models import Users
from projects.schemas import user_schema
import marshmallow


blueprint = Blueprint('users', __name__)


def check_token():
    authorization = request.headers.get('Authorizaration')

    if authorization is None:
        return False

    split_auth = authorization.split(' ')

    if len(split_auth) != 2:
        return False

    if split_auth[0] != 'Bearer':
        return False

    token = split_auth[1]

    try:
        jwt.decode(token, current_app.config['SECRET'])
        return True
    except:
        return False

def authentificater(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        check_response = check_token()

        if check_response is False:
            return 'Unauthorized', 401

        return f(check_response, *args, **kwargs)

    return wrapper


@blueprint.route('/register', methods=['POST'])
@blueprint.route('/users', methods=['POST'])
def register():
    user = user_schema.load(request.json)

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), 201


@blueprint.route('/users', methods=['GET'])
@authentificater
def list_users(payload):
    users = Users.query.all()

    return jsonify(user_schema.dump(users, many=True)), 200


@blueprint.route('/users/<id>', methods=['GET'])
@authentificater
def view_user(payload, id):
    if str(payload['sub']) != str(id):
        return 'Forbidden', 403

    user = Users.query.get_or_404(id)

    return user_schema.dump(user), 200


@blueprint.route('/users/<id>', methods=['PUT'])
@authentificater
def update_user(payload, id):
    user = Users.query.get_or_404(id)
    user = user_schema.load(
        data=request.json,
        instance=user,
        partial=False
    )

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), 200


@blueprint.route('/users/<id>', methods=['PATCH'])
@authentificater
def patch_user(payload, id):
    user = Users.query.get_or_404(id)
    user = user_schema.load(
        data=request.json,
        instance=user,
        partial=True
    )

    db.session.add(user)
    db.session.commit()

    return user_schema.dump(user), 200


@blueprint.route('/users/<id>', methods=['DELETE'])
@authentificater
def delete_user(payload, id):
    user = user.query.get_or_404(id)

    db.session.delete(user)
    db.session.commit()

    return '', 204


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    data = request.get_json()

    mail = data.get('mail')
    password = data.get('password')

    user = Users.query.filter_by(mail=mail).first()

    if user is None:
        return 'Not found', 404


    if bcrypt.check_password_hash(user.password, password) is False:
        return 'Not Found', 404


    payload = {
        'sub': user.id,
        'name': user.name,
        'iat': datetime.now()
    }

    return jwt.encode(
        payload,
        current_app.config['SECRET'],
        algorithm='HS256'
    )
