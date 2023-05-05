from flask import Blueprint, abort, request, jsonify, flash, make_response, url_for
from .term import Term
from ..dbmanager import get_db
bp = Blueprint("term-api", __name__, url_prefix="/api/terms")

@bp.route("", methods = ["GET","POST"])
def post_terms():
    page_num = 1
    if request.method == "POST":
        json_term = request.json
        if json_term:
            try:
                term = Term.from_json(json_term)
                get_db().add_term(term)
                #making response
                resp = make_response({}, 201)
                term_id = get_db().get_term_id()
                resp.headers["Location"] = url_for("term-api.term", term_id = term_id)
                return resp
            except Exception:
                flash("could not add term")
                abort(409)
    elif request.method == "GET":
        if request.args:
            page = request.args.get("page") 
            if page:
                page_num = int(page)     
    try:            
        terms, prev_page, next_page = get_db().get_terms(page_num = page_num, page_size = 5)            
        json_terms = {
            "previous_page" : prev_page,
            "next_page": next_page,
            "results" : [term.to_json() for term in terms]}
        return jsonify(json_terms)
    except:
        flash("could not fetch terms")
        abort(404)
        
@bp.route("/<int:term_id>", methods = [ "DELETE", "PUT", "GET"])
def term(term_id):
    if request.method == "PUT":
        json_term = request.json
        if json_term:
            try:
                term = Term.from_json(json_term)
                if term.id != None:
                    get_db().update_term(term)
                    resp = make_response({}, 200)
                    return resp
                else: 
                    get_db().add_term(term)
                    #making response
                    resp = make_response({}, 201)
                    term_id = get_db().get_term_id()
                    resp.headers["Location"] = url_for("term-api.term", term_id = term_id)
                    return resp
            except Exception as e:
                flash("could not add term")
                abort(409)
    elif request.method == "DELETE":
        try:
            term = get_db().get_term(int(term_id))
            if term == None:
                abort(404)
            else:
                get_db().delete_term(int(term_id))
                resp = make_response({}, 204)
                return resp
        except:
            abort(403)
            
    elif request.method == "GET":    
        try:
            term = get_db().get_term(int(term_id))
            return term.to_json()
        except:
            flash("Invalid ID, make sure url is correct")
            abort(404)
   