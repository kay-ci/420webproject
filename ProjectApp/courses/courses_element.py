class CourseElement:
    def __init__ (self, course_id, element_id, hours):
        if not isinstance (course_id, str):
            raise Exception ("course id is not a str")
        if not isinstance (element_id, str):
            raise Exception ("Element id is not str")
        if not isinstance (hours, int) or not isinstance(hours, float):
            raise Exception ("hours is not int or float")
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
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired
class CourseElementForm:
    course_id = StringField('Course ID', [DataRequired()])
    element_id = StringField('Element ID', [DataRequired()])
    hours = FloatField('Hours', [DataRequired()])