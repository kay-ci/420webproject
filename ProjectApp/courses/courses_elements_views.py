from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from .courses_element import CourseElement, CourseElementForm
from ..dbmanager import get_db
from flask_login import login_required

bp = Blueprint("courses_elements", __name__, url_prefix="/courses-elements")

@bp.route("/delete/<course_id>/<element_id>", methods=["GET"])
@login_required
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
    if request.method == "POST":
        if form.validate_on_submit():
            if get_db().get_course(form.course_id.data) == None:
                raise ValueError("couldn't find course with that course id")
            try:
                new_course_element = CourseElement(form.course_id.data, int(form.element.data), float(form.hours.data))
                if(float(form.hours.data) < 0):
                    raise Exception()
            except Exception:
                flash("your hours is of wrong format")
                return redirect(url_for('courses_elements.list_courses_elements'))
            if get_db().get_course_element(form.course_id.data, int(form.element.data)) == None:
                get_db().add_courses_element(new_course_element)
                flash("successfully added new course element connection")
            else:
                get_db().update_courses_element(new_course_element)
                flash("successfully updated the hours of that course element connection")
        else:
            flash("something's wrong with the form")
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
    return render_template("courses_elements.html", courses_elements = get_db().get_courses_elements(page_size, page)[0], form = form, course_ids= get_db().get_elements_course_ids_with_hours(page_size, page), page = page, page_size = page_size)
