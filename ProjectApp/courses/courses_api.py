from flask import Blueprint, flash, jsonify, render_template, request, abort, make_response, url_for
from .course import Course
from ..dbmanager import get_db
bp = Blueprint('courses_api', __name__, url_prefix="/api/courses")

@bp.route("/show", methods = ["GET"])
def get_courses():
    page_num = 1
    if request.method == "GET":
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

@bp.route("/addcourse", methods = ["GET","POST"])
def add_course():
    if request.method == 'POST':
        result = request.json
        if result:
            try:
                course = Course.from_json(result)
                get_db().add_course(course)
                resp = make_response({}, 201)
                return resp
            except Exception as e:
                abort(409)
    elif request.method == "GET":
        try:            
            courses, prev_page, next_page = get_db().get_courses(page_num = 1, page_size = 10)            
            json_courses = {
                "previous_page" : prev_page,
                "next_page": next_page,
                "results" : [course.to_json() for course in courses]}
            return jsonify(json_courses)
        except Exception as e:
            abort(404)
        
    



@bp.route("/update-course", methods = ["GET","PUT"])
def update_course():
    if request.method == 'PUT':
        result = request.json
        if result:
            course = Course.from_json(result)
            try:
                get_db().update_course(course)
            except Exception as e:
                flash("course does not exist")
                abort(409)
    try:            
        courses, prev_page, next_page = get_db().get_courses()
        json_courses = [course.to_json() for course in courses]
        return jsonify(json_courses)
    except:
        flash("Could not fetch Courses")
        
@bp.route("/delete-course", methods = ["GET","DELETE"])
def delete_course():
    if request.method == 'DELETE':
        if request.args:
            id = request.args.get("id")
            try:
                get_db().del_course(str(id))
            except Exception as e:
                flash("could not Delete Course")
                abort(409)
