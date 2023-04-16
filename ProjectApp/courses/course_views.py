from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from ProjectApp.dbmanager import get_db
from .course import Course, CourseForm


bp = Blueprint('courses', __name__, url_prefix='/courses/')

@bp.route("/", methods=['GET', 'POST'])
def list_courses():
    form = CourseForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            course = Course(form.name.data, form.street.data, form.city.data, form.province.data)
            result = [name for name in get_db().get_courses() if name.course_id == course.course_id and name.course_title == course.course_title]
            if len(result) == 0:
                get_db().add_course(course)
            else:
                flash('Course already exists')
        elif request.method == 'GET':
            return render_template('courses.html', form = form, courses = get_db().get_courses())
        return render_template('courses.html', form = form, courses = get_db().get_courses())
    except Exception as e:
        print(e)
        return render_template('404.html')

@bp.route("/<string:the_id>/")
def find_course(the_id):
    try:
        result = get_db().get_course(the_id)
        i = result.domain_id
        return render_template('course.html', course = result, term = get_db().get_term(result.term_id), domain = get_db().get_domain(result.domain_id))
    except Exception as e:
        flash('Something went wrong, could not find the Course')
        # return redirect(url_for('courses.list_courses'))
