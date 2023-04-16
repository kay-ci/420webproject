class Element:
    def __init__(self, element_id, element_order, element, element_criteria, competency_id):
        #element id is nullable
        if not isinstance (element_order, int):
            raise Exception ("element_order not int")
        if not isinstance (element, str):
            raise Exception ("element not str")
        if not isinstance (element_criteria, str):
            raise Exception ("element_criteria not str")
        if not isinstance (competency_id, str):
            raise Exception ("competency_id not str")
        self.element_id = element_id
        self.element_order = element_order
        self.element = element
        self.element_criteria = element_criteria
        self.competency_id = competency_id
        
    def __repr__(self):
        return f'Element({self.element_id}, {self.element_order}, {self.element}, {self.element_criteria}, {self.competency_id})'
    
    def __str__(self):
        return f'{self.element_id} {self.element_order} {self.element_order} {self.element} {self.element_criteria} {self.competency_id}'
    
    def to_json():
        pass
    
    def from_json(element_str):
        if not isinstance (element_str, dict):
            raise Exception ("Expected type dict")
        ##return Element
        
from flask_wtf import FlaskForm 
from wtforms import StringField
from wtforms.validators import DataRequired
class ElementForm(FlaskForm):
    element_id = StringField('Element id', validators=[DataRequired()])
    element_order = StringField('Element_order', validators=[DataRequired()])
    element = StringField('Element', validators=[DataRequired()])
    element_criteria = StringField('Element criteria', validators=[DataRequired()])
    competency_id = StringField('Competency_id',validators=[DataRequired()])
        
