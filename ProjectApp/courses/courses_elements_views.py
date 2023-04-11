from flask import Blueprint, abort, render_template, redirect, url_for, flash, request
from .courses_element import CourseElement, CourseElementForm
from ..dbmanager import get_db

bp = Blueprint('Course_element', __name__, url_prefix='/courses-element/')

bp.route("/", methods = ['GET', ['POST']])
def list_courses_elements():
    if request.method == 'GET':
        return render_template('courses_elements.html', courses_elements = get_db().get_courses_elements())