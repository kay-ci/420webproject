from flask import Blueprint, jsonify, request
from ..dbmanager import get_db
from .term import Term
bp = Blueprint('terms_api', __name__, url_prefix='/api/terms/')

@bp.route('/', methods=['GET', 'POST'])
def terms_api():
    if request.method == 'GET':
        if request.args:
            id = request.args.get("id")
            terms = get_db().get_terms()
            term = [term for term in terms if term.id == id]
            return jsonify(term[0].__dict__)
    terms = get_db().get_terms()
    json = [term.__dict__ for term in terms]
    return jsonify(json)
