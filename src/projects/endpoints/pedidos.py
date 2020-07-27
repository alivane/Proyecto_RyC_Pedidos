from datetime import datetime
import jwt
from functools import wraps
from flask import request, jsonify, Blueprint, current_app
from projects import db, bcrypt
from projects.models import ( Pedidos )
from projects.schemas import ( pedidos_schema )
import marshmallow


blueprint = Blueprint('pedidos', __name__)


def check_token():
    authorization = request.headers.get('Authorization')

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


## ==============PEDIDOS================

@blueprint.route('/add_pedido', methods=['POST'])
@authentificater
def add_pedido(payload):
    pedido = pedidos_schema.load(request.json)

    db.session.add(pedido)
    db.session.commit()

    return pedidos_schema.dump(pedido), 201


@blueprint.route('/get_pedidos', methods=['GET', 'POST'])
@authentificater
def get_pedidos(payload):
    pedidos = Pedidos.query.all()

    return jsonify(pedidos_schema.dump(pedidos, many=True)), 200


@blueprint.route('/get_pedidos_filter/<terminated>', methods=['GET', 'POST'])
@authentificater
def get_pedidos_filter(payload, terminated):
    pedidos = Pedidos.query.filter_by(terminated=terminated).all()
    return jsonify(pedidos_schema.dump(pedidos, many=True)), 200


@blueprint.route('/update_pedidos/<id>', methods=['PUT'])
@authentificater
def update_pedidos(payload, id):
    pedidos = Pedidos.query.get_or_404(id)
    pedidos = pedidos_schema.load(
        data=request.json,
        instance=pedidos,
        partial=True
    )

    db.session.add(pedidos)
    db.session.commit()

    return pedidos_schema.dump(pedidos), 200

@blueprint.route('/get_pedido_id/<id>', methods=['GET', 'POST'])
@authentificater
def get_one_week_menu(payload, id):
    pedidos = Pedidos.query.get_or_404(id)

    return pedidos_schema.dump(pedidos), 200