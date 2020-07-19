from flask import Blueprint


blueprint = Blueprint('status', __name__)

@blueprint.errorhandler(404)
def not_found(err):
    return '<h1>Error</h1>'


@blueprint.route('/')
def index():
    return '<h1>OK</h1>'
