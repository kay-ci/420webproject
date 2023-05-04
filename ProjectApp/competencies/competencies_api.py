#returned json obj should contain a url key for itself.
#returning a collection should return list of obj, not just url to them
#returning a collection should include: count of all entries, url to previous page, url to next page, and results
#GET POST for collections, GET PUT DELETE for document

from flask import Blueprint, jsonify, request, make_response
from ..dbmanager import get_db
from .competency import Competency
bp = Blueprint('competencies_api', __name__, url_prefix='/api/competencies/')

@bp.route('/', methods=['GET', 'POST'])
def competencies_api():
    page_num = 1
    if request.method == 'POST':
        competency_json = request.json
        if not isinstance(competency_json, dict):
            raise TypeError("expecting a dict/json")
        if competency_json:
            competency = Competency.from_json(competency_json)
            get_db().add_competency(competency)#what if competency id already used?
            #aren't we supposed to return url key
    elif request.method == 'GET':
        if request.args:
            page = request.args.get("page")
            if page:
                page_num = int(page)
    competencies, prev_page, next_page = get_db().get_competencies(page_num=page_num, page_size=5)
    json = {'prev_page': prev_page, 
            'next_page': next_page, 
            'results':[competency.__dict__ for competency in competencies]}
    return jsonify(json)

@bp.route('/<competency_id>', methods = ["GET", "PUT", "DELETE"])
def competency_api(competency_id):
    if request.method == "DELETE":
        try:
            get_db().delete_competency(competency_id)
            response = make_response({}, 204)
            return response
        except ValueError() as e:
            response = make_response({"id":404, "description":str(e)}, 404)
            return response
        
@bp.route('/<competency_id>/', methods=["GET","POST"])
def competency_elements_api():
    pass

@bp.route('/competency_id/<int:element_id>', methods=["GET", "PUT", "DELETE"])
def competency_element_api():
    pass