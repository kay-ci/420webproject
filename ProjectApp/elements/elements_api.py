from flask import Blueprint, abort, request, jsonify, flash, make_response, url_for
from .element import Element
from ..dbmanager import get_db
bp = Blueprint("element-api", __name__, url_prefix="/api/elements")

@bp.route("", methods = ["GET","POST"])
def post_elements():
    page_num = 1
    if request.method == "POST":
        json_element = request.json
        if json_element:
            try:
                element = Element.from_json(json_element)
                get_db().add_element(element)
                #making response
                resp = make_response({}, 201)
                element_id = get_db().get_element_id()
                resp.headers["Location"] = url_for("element-api.element", element_id = element_id)
                return resp
            except Exception as e:
                flash("could not add element")
                abort(409)
    elif request.method == "GET":
        if request.args:
            page = request.args.get("page")
            try:
                if page:
                    page_num = int(page)
            except:
                flash("element with that id not found")
                abort(404)
    try:            
        elements, prev_page, next_page = get_db().get_elements(page_num = page_num, page_size = 10)            
        json_elements = {
            "previous_page" : prev_page,
            "next_page": next_page,
            "results" : [element.to_json() for element in elements]}
        return jsonify(json_elements)
    except:
        flash("could not fetch elements")
        abort(404)
        
@bp.route("/<int:element_id>", methods = [ "DELETE", "PUT", "GET"])
def element(element_id):
    if request.method == "PUT":
        json_element = request.json
        if json_element:
            try:
                element = Element.from_json(json_element)
                if element.element_id != None:
                    get_db().update_element(element)
                    resp = make_response({}, 200)
                    return resp
                else: 
                    get_db().add_element(element)
                    #making response
                    resp = make_response({}, 201)
                    element_id = get_db().get_element_id()
                    resp.headers["Location"] = url_for("element-api.element", element_id = element_id)
                    return resp
            except Exception as e:
                flash("could not add element")
                abort(409)
    elif request.method == "DELETE":
        try:
            element = get_db().get_element(int(element_id))
            if element == None:
                abort(404)
            else:
                get_db().delete_element(int(element_id))
                resp = make_response({}, 204)
                return resp
        except:
            abort(404)
            
    elif request.method == "GET":    
        try:
            element = get_db().get_element(int(element_id))
            return element.to_json()
        except:
            flash("Invalid ID, make sure url is correct")
            abort(404)
   