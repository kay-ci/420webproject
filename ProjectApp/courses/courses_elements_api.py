from flask import Blueprint, flash, jsonify, render_template, request, abort, make_response, url_for
from .courses_element import CourseElement
from ..dbmanager import get_db
bp = Blueprint('course_elements_api', __name__, url_prefix="/api/course-elements/")

@bp.route("/", methods = ["GET", "POST"])
def get_course_elements():
    if request.method == 'POST':
        result = request.json
        if result:
            if not isinstance(result, dict):
                return make_response({"description":"expecting json format"}, 400)
            try:
                course_element = CourseElement.from_json(result)
                get_db().add_courses_element(course_element)
                resp = make_response({}, 201)
                resp.headers["Location"] = url_for("course_elements_api.course_element_api", course_id = course_element.course_id, element_id = course_element.element_id)
                return resp
            except Exception as e:
                abort(409)
    elif request.method == "GET":
        if request.args:
            course_id = request.args.get("course_id")
            element_id = request.args.get("element_id")
            course = get_db().get_courses_element(str(course_id), int(element_id))
            if course:
                return course.to_json(), 200
            else:
                abort(404)
    page_num = 1
    try:            
        course_elements, prev_page, next_page = get_db().get_courses_elements(page = page_num, page_size = 10)            
        json_course_elements = {
            "previous_page" : prev_page,
            "next_page": next_page,
            "results" : [course_element.to_json() for course_element in course_elements]}
        return jsonify(json_course_elements)
    except Exception as e:
        flash(str(e))
        abort(404)




@bp.route("/<course_id>/<element_id>", methods = ["GET","PUT","DELETE"])
def course_element_api(course_id, element_id):
    if request.method == 'PUT':
        result = request.json
        if result:
            if not isinstance(result, dict):
                return make_response({"description":"expecting json format"}, 400)
            try:
                course_element = CourseElement.from_json(result)
                get_db().update_courses_element(course_element)
                resp = make_response({}, 204)
                resp.headers["Location"] = url_for("course_elements_api.course_element_api", course_id = course_element.course_id, element_id = course_element.element_id)
                return resp
            except Exception as e:
                abort(409)
    if request.method == 'DELETE':
        try:
            get_db().delete_courses_element(str(course_id), int(element_id))
            resp = make_response({}, 204)
            resp.headers["Location"] = url_for("course_elements_api.get_course_elements")
            return resp
        except Exception as e:
            abort(409)
    if request.method == "GET":
        course_element = get_db().get_courses_element(str(course_id), int(element_id))
        if course_element:
            return course_element.to_json(), 200
        else:
            abort(404)