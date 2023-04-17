class CourseElement:
    def __init__ (self, course_id, element_id, hours):
        if not isinstance (course_id, str):
<<<<<<< HEAD
            raise Exception ("course id is not a str")
        if not isinstance (element_id, int):
            raise Exception ("Element id is not an int")
=======
            raise Exception ("course id is not a string")
        if not isinstance (element_id, int):
            raise Exception ("Element id is not number")
>>>>>>> 313ab3297152e6c44019677b185e418a37b651e0
        if not isinstance(hours, float):
            raise Exception ("hours is not int or float")
        self.course_id = course_id
        self.element_id = element_id
        self.hours = hours
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
class CourseElementForm(FlaskForm):
    course_id = StringField('Course ID', [DataRequired()])
    element_id = StringField('Element ID', [DataRequired()])
    hours = FloatField('Hours', [DataRequired()])