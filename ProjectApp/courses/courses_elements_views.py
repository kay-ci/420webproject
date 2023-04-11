from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from .courses_element import CourseElement, CourseElementForm
from ..dbmanager import get_db

bp = Blueprint("courses_elements", __name__, url_prefix="/coursesElements")

@bp.route("/", methods = ["GET", "POST"])
def list_courses_elements():
    form = CourseElementForm()
    if request.method == "POST" and form.validate_on_submit():
        new_course_element = CourseElement(form.course_id, form.element_id, form.hours)
        try:
            get_db().add_courses_element(new_course_element)
        except ValueError as e:
            flash(e)
    if request.method == "GET":
        return render_template("courses_elements.html", courses_elements = get_db().get_courses_elements(), form = form)