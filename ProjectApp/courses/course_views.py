from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from .course import Course, CourseForm

bp = Blueprint('course', __name__, url_prefix='/courses/')

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
            return render_template('courses.html', form = form, addresses = get_db().get_courses())
        return render_template('course.html', form = form, addresses = get_db().get_courses)
    except Exception as e:
        return render_template('404.html')
