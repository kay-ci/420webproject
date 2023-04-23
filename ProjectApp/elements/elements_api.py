from flask import Blueprint, abort, request, jsonify, flash
from .element import Element
from ..dbmanager import get_db

bp = Blueprint('element-api', __name__, url_prefix='/api/elements/')

@bp.route('/', methods=['GET', 'POST'])
def elements_api():
    pass