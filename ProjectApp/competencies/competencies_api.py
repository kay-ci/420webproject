#returned json obj should contain a url key for itself.
#returning a collection should return list of obj, not just url to them
#returning a collection should include: count of all entries, url to previous page, url to next page, and results
#GET POST for collections, GET PUT DELETE for document

from flask import Blueprint, jsonify, request, make_response, url_for
from ..dbmanager import get_db
from .competency import Competency
from ..elements.element import Element
bp = Blueprint('competencies_api', __name__, url_prefix='/api/competencies')

@bp.route('', methods=['GET', 'POST'])
def competencies_api():
    page_num = 1
    if request.method == 'POST':
        competency_json = request.json
        if not isinstance(competency_json, dict):
            return make_response({"description":"expecting json format"}, 400)
        if not competency_json:
            return make_response({"description":"expecting a not empty json"}, 400)
        if not competency_json["elements"]:#empty list will match this condition too
            return make_response({"description":"competencies must be created with elements, expecting elements key for a list of element object with 'element' and 'element_criteria' keys"}, 400)
        try:
            competency = Competency.from_json(competency_json)
            get_db().add_competency(competency)#if id already used, will return 400 with str(e)
            order = 0
            for element in competency_json["elements"]:
                order+=1
                element = Element(None, order, element['element'], element['element_criteria'], competency.id)
                get_db().add_element(element)
            resp = make_response({}, 201)
            resp.headers["Location"] = url_for("competencies_api.competency_api", competency_id = competency.id)
            return resp
        except ValueError as e:
            return make_response({"description":str(e)}, 400)    
    elif request.method == 'GET':
        if request.args:
            page = request.args.get("page")
            if page:
                page_num = int(page)
    competencies, prev_page, next_page = get_db().get_competencies(page_num=page_num, page_size=5)
    json = {'prev_page': prev_page, 
            'next_page': next_page, 
            'results':[competency.__dict__ for competency in competencies]}
    return make_response(json, 200)

@bp.route('/<competency_id>', methods = ["GET", "PUT", "DELETE"])
def competency_api(competency_id):
    if len(competency_id) > 4:
        return make_response({"description":"competency id has a max length of 4 characters"}, 404)
    if request.method == "DELETE":
        try:
            get_db().delete_competency(competency_id)
            response = make_response({}, 204)
            return response
        except ValueError as e:
            response = make_response({ "description":str(e)}, 404)
            return response
    if request.method == "PUT":
        competency_json = request.json
        if not isinstance(competency_json, dict):
            return make_response({"description":"expecting json format"}, 400)
        if not competency_json:
            return make_response({"description":"expecting a not empty json"}, 400)
        if get_db().get_competency(competency_id) == None:#then we add
            if not competency_json["elements"]:#empty list will match this condition too
                return make_response({"description":"competencies must be created with elements, expecting elements key for a list of element object with 'element' and 'element_criteria' keys"}, 400)
            try:
                competency = Competency.from_json_without_id(competency_json, competency_id)
                get_db().add_competency(competency)
                order = 0
                for element in competency_json["elements"]:
                    order+=1
                    element = Element(None, order, element['element'], element['element_criteria'], competency_id)
                    get_db().add_element(element)
                resp = make_response({}, 201)
                resp.headers["Location"] = url_for("competencies_api.competency_api", competency_id = competency_id)
                return resp
            except ValueError as e:
                return make_response({"description":str(e)}, 400)
        else:#if given id corresponds to a competency
            try:
                competency = get_db().get_competency(competency_id)
                if competency_json["competency"]:
                    competency.competency = competency_json["competency"]
                if competency_json["competency_achievement"]:
                    competency.competency_achievement = competency_json["competency_achievement"]
                if competency_json["competency_type"]:
                    if competency_json["competency_type"] != "Mandatory" and competency_json["competency_type"] != "Optional":
                        return make_response({"description":"competency_type has to be 'Mandatory' or 'Optional'"}, 400)
                    competency.competency_type = competency_json["competency_type"]
                competency = Competency.from_json_without_id(competency_json, competency_id)
                get_db().update_competency(competency.id, competency.competency, competency.competency_achievement, competency.competency_type)#if id already used, will return 400 with str(e)
                resp = make_response({}, 201)
                resp.headers["Location"] = url_for("competencies_api.competency_api", competency_id = competency_id)
                return resp
            except ValueError as e:
                return make_response({"description":str(e)}, 400)
    elif request.method == "GET":
        if get_db().get_competency(competency_id) == None:
            return make_response({"description":"could not find competency for this id"}, 404)
        json = get_db().get_competency(competency_id).__dict__
        elements = get_db().get_competency_elements(competency_id)
        elements_url = []
        for element in elements:
            elements_url.append(url_for('element.show_element', element_id = element.element_id))
        json["elements"] = elements_url
        return make_response(json, 200)