class CourseElement:
    def __init__ (self, course_id, element_id, hours):
        if not isinstance (course_id, str):
            raise Exception ("course id is not a str")
        if not isinstance (element_id, int):
            raise Exception ("Element id is not an int")
        if not isinstance(hours, float):
            raise Exception ("hours is not int or float")
        from ..dbmanager import get_db
        self.course_id = course_id
        self.element_id = element_id
        self.course = get_db().get_course(course_id)
        self.element = get_db().get_element(element_id)
        self.hours = hours
        self.calculated_total_hours = get_db().calculate_course_hours(course_id)

    def __repr__(self):
        return f'CourseElement({self.course_id}, {self.element_id}, {self.hours})'
    def __str__(self):
        return f'{self.course_id} {self.element_id} {self.hours}'
    def to_json():
        pass
    def from_json(course_element_str):
        if not isinstance (course_element_str, dict):
            raise Exception ("Expected type dict")
        return CourseElement(course_element_str['course_id'], course_element_str['element_id'], course_element_str['hours'])
    
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class CourseElementForm(FlaskForm):
    course_id = StringField('Course ID', [DataRequired()])
    element_id = DecimalField('Element ID', [DataRequired()])
    hours = FloatField('Hours', [DataRequired()])