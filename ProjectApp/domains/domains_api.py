from flask import Blueprint, jsonify, request
from dbmanager import get_db
from .domain import Domain
bp = Blueprint('domains_api', __name__, url_prefix='/api/domains/')

@bp.route('/', methods=['GET','POST'])
def domains_api():
    if request.method == 'POST':
        domain_json = request.json
        if domain_json:
            domain = Domain.from_json(domain_json)
            get_db().insert_domain(domain)
    elif request.method == 'GET':
        if request.args:
            domain_id = request.args.get("domain_id")
            domains = get_db().get_domains()
            domain = [domain for domain in domains if domain.id == domain_id]
            return jsonify(domain[0].__dict__)
    domains = get_db().get_domains()
    json = [domain.__dict__ for domains in domains]
    return jsonify(json)

    
    