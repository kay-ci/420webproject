
class Course:
    def __init__(self, course_id, course_title, theory_hours, work_hours, lab_hours, description, domain_id, term_id):
        
        if not isinstance(course_id, str):
            raise Exception("course id must be a string")
        if not isinstance(course_title, str):
            raise Exception("course title must be a string")
        if not isinstance(theory_hours, float):
            raise Exception("theory hours must be a float")
        if not isinstance(lab_hours, float):
            raise Exception("lab hours must be a float")
        if not isinstance(work_hours, float):
            raise Exception("work hours must be a float")
        if not isinstance(description, str):
            raise Exception("description must be a string")
        if not isinstance(domain_id, int):
            raise Exception("domain id must be an integer")
        if not isinstance(term_id, int):
            raise Exception("term id must be an integer")

        self.course_id = course_id
        self.course_title = course_title
        self.theory_hours = theory_hours
        self.lab_hours = lab_hours
        self.work_hours = work_hours
        self.description = description
        self.domain_id = domain_id
        self.term_id = term_id
        
    def __repr__(self):
        return f'Course({self.course_id}, {self.course_title}, {self.theory_hours}, {self.lab_hours}, {self.work_hours}, {self.description}, {self.domain_id}, {self.term_id})'
        
    def __str__(self):
        value = f'{self.course_title}: {self.course_id}, {self.theory_hours}, {self.lab_hours}, {self.work_hours}, {self.description}, {self.domain_id}, {self.term_id}'
        return value
    
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
    
class CourseForm(FlaskForm):
    course_id = StringField('course_id', validators=[DataRequired()])
    course_title = StringField('course_title', validators=[DataRequired()])
    thoery_hours = IntegerField('thoery_hours', validators=[DataRequired()])
    lab_hours = IntegerField('lab_hours', validators=[DataRequired()])
    work_hours = IntegerField('work_hours', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    domain_id = IntegerField('domain_id', validators=[DataRequired()])
    term_id = IntegerField('term_id', validators=[DataRequired()])