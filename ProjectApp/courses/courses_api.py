from flask import Blueprint, flash, jsonify, render_template, request
from course import Course
bp = Blueprint('courses_api', __name__, url_prefix='/api/courses/')
