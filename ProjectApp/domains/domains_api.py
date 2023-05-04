from flask import Blueprint, jsonify, request
from ProjectApp.dbmanager import get_db
from .domain import Domain
bp = Blueprint('domains_api', __name__, url_prefix='/api/domains/')

def posts_api():
    page_num = 1
    if request.method == 'POST':
        domain_json = request.json
        if domain_json:
            domain = Domain.from_json(domain_json)
            get_db().add_domain(domain)
    elif request.method == 'GET':
        if request.args:
            page = request.args.get("page")
            if page:
                page_num = int(page)
    posts, prev_page, next_page = get_db().get_posts(page_num=page_num, page_size=10)
    json = {'prev_page': prev_page, 
            'next_page': next_page, 
            'results':[post.__dict__ for post in posts]}
    return jsonify(json)


@bp.route('/delete-domain/', methods = ["DELETE"])
def delete_domain():
    pass
    

@bp.route('/update-domain', methods = ["PUT"])
def update_domain():
    pass
    
    