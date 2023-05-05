from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from .courses_element import CourseElement, CourseElementForm
from ..dbmanager import get_db

bp = Blueprint("courses_elements", __name__, url_prefix="/courses-elements")

@bp.route("/delete/<course_id>/<element_id>", methods=["GET"])
def delete_course_element(course_id, element_id):
    element_id = int(element_id)
    if get_db().get_course_element(course_id, element_id) == None:
        flash("course element connection not found")
        abort(404)
    get_db().delete_course_element(course_id, element_id)
    return redirect(url_for('courses_elements.list_courses_elements'))

@bp.route("/", methods = ["GET", "POST"])
def list_courses_elements(page=1, page_size=10):
    form = CourseElementForm()
    elements = get_db().get_elements()[0]
    for element in elements:
        form.element.choices.append((element.element_id, f"{element.element} ({element.competency_id})"))
    if request.method == "POST" and form.validate_on_submit():
        if get_db().get_course(form.course_id.data) == None:
            raise ValueError("couldn't find course with that course id")
        new_course_element = CourseElement(form.course_id.data, int(form.element.data), float(form.hours.data))
        if get_db().get_course_element(form.course_id.data, int(form.element.data)) == None:
            get_db().add_courses_element(new_course_element)
            flash("successfully added new course element connection")
        else:
            get_db().update_courses_element(new_course_element)
            flash("successfully updated the hours of that course element connection")
    try:
        page = int(request.args["page"])
    except Exception:
        page = 1
    try:
        page_size = int(request.args["page_size"])
    except Exception:
        page_size = 10
    if page < 1 or page_size < 1:
        abort(404)
    return render_template("courses_elements.html", courses_elements = get_db().get_courses_elements(page_size, page), form = form, course_ids= get_db().get_elements_course_ids_with_hours(page_size, page), page = page, page_size = page_size)
    
#display all elements for a given course
@bp.route("course/<element_id>/")
def get_course_element_id(element_id):
    pass
    
#display a course for a given element_id
@bp.route("elements/<course_id>/")
def get_course_course_id(course_id):
    pass