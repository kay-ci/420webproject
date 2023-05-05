from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from .courses_element import CourseElement, CourseElementForm
from ..dbmanager import get_db

bp = Blueprint("courses_elements", __name__, url_prefix="/courses-elements")

@bp.route("/", methods = ["GET", "POST"])
def list_courses_elements(page=1, page_size=10):
    form = CourseElementForm()
    if request.method == "POST" and form.validate_on_submit():
        new_course_element = CourseElement(form.course_id.data, int(form.element_id.data), float(form.hours.data))
        try:
            get_db().add_courses_element(new_course_element)
        except ValueError as e:
            flash(e)
    try:
        page = int(request.args["page"])
    except Exception:
        page = 1
    try:
        page_size = int(request.args["page_size"])
    except Exception:
        page_size = 10
    elements, prev_page, next_page = get_db().get_elements(page, page_size)
    return render_template("courses_elements.html", courses_elements = get_db().get_courses_elements(page_size, page), form = form, course_ids = get_db().get_elements_course_ids(page_size, page), page = page, page_size = page_size, elements = elements)

#display all elements for a given course
@bp.route("course/<element_id>/")
def get_course_element_id(element_id):
    pass
    
#display a course for a given element_id
@bp.route("elements/<course_id>/")
def get_course_course_id(course_id):
    pass