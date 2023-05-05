from flask import Blueprint, flash, jsonify, render_template, request, abort, make_response, url_for
from .course import Course
from ..dbmanager import get_db
bp = Blueprint('courses_api', __name__, url_prefix="/api/courses/")

@bp.route("/", methods = ["GET", "POST"])
def get_courses():
    page_num = 1
    if request.method == 'POST':
        result = request.json
        if result:
            if not isinstance(result, dict):
                return make_response({"description":"expecting json format"}, 400)
            try:
                course = Course.from_json(result)
                get_db().add_course(course)
                resp = make_response({}, 201)
                resp.headers["Location"] = url_for("courses_api.course_api", course_id = course.course_id)
                return resp
            except Exception as e:
                abort(409)
    elif request.method == "GET":
        if request.args:
            id = request.args.get("id")
            course = get_db().get_course(str(id))
            if course:
                return course.to_json(), 200
            else:
                abort(404)
    try:            
        courses, prev_page, next_page = get_db().get_courses(page_num = page_num, page_size = 10)            
        json_courses = {
            "previous_page" : prev_page,
            "next_page": next_page,
            "results" : [course.to_json() for course in courses]}
        return jsonify(json_courses)
    except Exception as e:
        abort(404)


@bp.route("/<course_id>", methods = ["GET","PUT","DELETE"])
def course_api(course_id):
    if request.method == 'PUT':
        result = request.json
        if result:
            if not isinstance(result, dict):
                return make_response({"description":"expecting json format"}, 400)
            try:
                course = Course.from_json(result)
                get_db().update_course(course)
                resp = make_response({}, 204)
                resp.headers["Location"] = url_for("courses_api.course_api", course_id = course.course_id)
                return resp
            except Exception as e:
                abort(409)
    if request.method == 'DELETE':
        try:
            get_db().del_course(str(course_id))
            resp = make_response({}, 204)
            resp.headers["Location"] = url_for("courses_api.get_courses")
            return resp
        except Exception as e:
            flash("could not delete course")
            abort(409)
    if request.method == "GET":
        course = get_db().get_course(str(course_id))
        if course:
            return course.to_json(), 200
        else:
            abort(404)