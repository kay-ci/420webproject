from flask import Blueprint, abort, request, jsonify, flash, make_response, url_for
from .domain import Domain
from ..dbmanager import get_db
bp = Blueprint("domain-api", __name__, url_prefix="/api/domains")

@bp.route("", methods = ["GET","POST"])
def post_domains():
    page_num = 1
    if request.method == "POST":
        json_domain = request.json
        if json_domain:
            try:
                domain = Domain.from_json(json_domain)
                get_db().add_domain(domain)
                #making response
                resp = make_response({}, 201)
                domain_id = get_db().get_domain_id()
                resp.headers["Location"] = url_for("domain-api.domain", domain_id = domain_id)
                return resp
            except Exception as e:
                flash("could not add domain")
                abort(409)
    elif request.method == "GET":
        if request.args:
            page = request.args.get("page")
            try:
                if page:
                    page_num = int(page)
            except:
                flash("domain with that id not found")
                abort(404)
    try:            
        domains, prev_page, next_page = get_db().get_domains(page_num = page_num, page_size = 2)            
        json_domains = {
            "previous_page" : prev_page,
            "next_page": next_page,
            "results" : [domain.to_json() for domain in domains]}
        return jsonify(json_domains)
    except:
        flash("could not fetch domains")
        abort(404)
        
@bp.route("/<int:domain_id>", methods = [ "DELETE", "PUT", "GET"])
def domain(domain_id):
    if request.method == "PUT":
        json_domain = request.json
        if json_domain:
            try:
                domain = Domain.from_json(json_domain)
                if domain.domain_id != None:
                    get_db().update_domain(domain)
                    resp = make_response({}, 200)
                    return resp
                else: 
                    get_db().add_domain(domain)
                    #making response
                    resp = make_response({}, 201)
                    domain_id = get_db().get_domain_id()
                    resp.headers["Location"] = url_for("domain-api.domain", domain_id = domain_id)
                    return resp
            except Exception as e:
                flash("could not add domain")
                abort(409)
    elif request.method == "DELETE":
        try:
            domain = get_db().get_domain(int(domain_id))
            if domain == None:
                abort(404)
            else:
                get_db().delete_domain(int(domain_id))
                resp = make_response({}, 204)
                return resp
        except:
            abort(403)
            
    elif request.method == "GET":    
        try:
            domain = get_db().get_domain(int(domain_id))
            return domain.to_json()
        except:
            flash("Invalid ID, make sure url is correct")
            abort(404)
   
    
    