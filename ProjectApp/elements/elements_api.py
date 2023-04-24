from flask import Blueprint, abort, request, jsonify, flash
from .element import Element
from ..dbmanager import get_db
bp = Blueprint("element-api", __name__, url_prefix="/api/elements")

@bp.route("/", methods = ["GET"])
def get_elements():
    if request.method == "GET":
        if request.args:
            id = request.args.get("id")
            try:
                element = get_db().get_element(int(id))
                if element:
                    return element.to_json(), 200
                else:
                    abort(404)
            except:
                flash("element with that id not found")
                abort(404)
    try:            
        elements = get_db().get_elements()
        json_elements = [element.to_json() for element in elements]
        return jsonify(json_elements)
    except:
        flash("Could not fetch elements")

@bp.route("/add-element", methods= ["GET","POST"])
def add_element():
    if request.method == "POST":
        json_element = request.json
        if json_element:
            try:
                element = Element.from_json(json_element)
                get_db().add_element(element)
                flash("element added succesfully!")
                # display the added element
            except Exception as e:
                flash("could not add element")
                abort(409)
    try:            
        elements = get_db().get_elements()
        json_elements = [element.to_json() for element in elements]
        return jsonify(json_elements)
    except:
        flash("Could not fetch elements")