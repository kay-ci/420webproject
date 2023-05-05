from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from ProjectApp.dbmanager import get_db
from .course import Course, CourseForm, CourseFormPartial


bp = Blueprint('courses', __name__, url_prefix='/courses/')

@bp.route("/", methods=['GET', 'POST'])
def list_courses():
    form = CourseForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            course = Course(form.course_id.data, form.course_title.data, float(form.theory_hours.data), float(form.work_hours.data), float(form.lab_hours.data), form.description.data, int(form.domain_id.data), int(form.term_id.data))
            courses, prev_page, next_page = get_db().get_courses()
            result_course = [name for name in courses if name.course_id == course.course_id]
            if len(result_course) == 0:
                get_db().add_course(course)
            else:
                flash('Course already exists')
        elif request.method == 'GET':
            courses, prev_page, next_page = get_db().get_courses()
            return render_template('courses.html', form = form, courses = courses)
        return redirect(url_for('courses.list_courses'))
    except Exception as e:
        return render_template('404.html')

@bp.route("/<the_id>/", methods=['GET', 'POST'])
def find_course(the_id):
    try:
        course = get_db().get_course(the_id)
        term = get_db().get_term(course.term_id)
        domain = get_db().get_domain(course.domain_id)
        competencies = get_db().get_course_competency(course.course_id)
        elements = get_db().get_course_competency_element(course.course_id)
        
        form = CourseFormPartial()
        if request.method == 'POST' and form.validate_on_submit():
            new_course = Course(course.course_id, form.course_title.data, float(form.theory_hours.data), float(form.work_hours.data), float(form.lab_hours.data), form.description.data, int(form.domain_id.data), int(form.term_id.data))
            courses, prev_page, next_page = get_db().get_courses()
            old_course = [name for name in courses if name.course_id == new_course.course_id]
            if len(old_course) == 1:
                get_db().update_course(new_course)
                return redirect(url_for('courses.find_course', the_id = new_course.course_id))
        return render_template('course.html', course = course, term = term, domain = domain, competencies = competencies, elements = elements, form = form)
    except Exception as e:
        flash('Something went wrong, ' + str(e))
        return redirect(url_for('courses.list_courses'))

@bp.route('/delete/<id>/')
def delete_from_courses(id):
    try:
        get_db().del_course(id)
    except ValueError:
        flash("couldn't find Course to delete")
    return redirect(url_for('courses.list_courses'))
        