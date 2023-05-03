from flask import Blueprint, flash, jsonify, render_template, request, abort
from .course import Course
from ..dbmanager import get_db
bp = Blueprint('courses_api', __name__, url_prefix='/api/courses/')

@bp.route("/", methods = ["GET"])
def get_courses():
    courses = get_db().get_courses()
    if request.args:
        id = request.args.get("id")
        course = get_db().get_course(str(id))
        if course:
            return course.to_json(), 200
        else:
            flash('Could not Find Course in Database')
            abort(404)

    courses_json = [course.to_json() for course in courses]
    return courses_json, 200

        
@bp.route("/add-course/", methods = ["GET","POST"])
def add_course():
    if request.method == 'POST':
        result = request.json
        if result:
            course = Course.from_json(result)
            try:
                get_db().add_course(course)
            except Exception as e:
                flash("could not add Course")
                abort(409)
    try:            
        courses = get_db().get_courses()
        json_courses = [course.to_json() for course in courses]
        return jsonify(json_courses)
    except:
        flash("Could not fetch Courses")

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
        courses = get_db().get_courses()
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
