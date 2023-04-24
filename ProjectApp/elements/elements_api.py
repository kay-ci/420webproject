from flask import Blueprint, abort, request, jsonify, flash
from .element import Element
from ..dbmanager import get_db
bp = Blueprint("element-api", __name__, url_prefix="/api/elements")

@bp.route("/", methods = ["GET", "POST"])
def get_elements():
    if request.method == "GET":
        if request.args:
            id = request.args.get("id")
            try:
                element = get_db().get_element(int(id))
                if element:
                    return element.to_json(), 200
                else: 
                    return 400
            except:
                abort(404)
    elif request.method == "POST":
        200
    elements = get_db().get_elements()
    json_elements = [element.to_json() for element in elements]
    return jsonify(json_elements)