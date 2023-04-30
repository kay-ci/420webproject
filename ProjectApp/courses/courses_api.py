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
    return courses_json

        
@bp.route("/add-course", methods = ["GET","POST"])
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
            flash('Added Course to Database')
    try:            
        courses = get_db().get_courses()
        json_courses = [course.to_json() for course in courses]
        return jsonify(json_courses)
    except:
        flash("Could not fetch Courses")

