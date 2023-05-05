class Term:
    def __init__(self, id, name):
        if not isinstance(id, int) and id != None:
            raise TypeError("expecting an id of type int")
        if not isinstance(name, str):
            raise TypeError("expecting a name of type str")
        self.id = id
        self.name = name
    def __repr__(self):
        return f"{self.id}({self.name})"
    def __str__(self):
        return f"{self.id}: {self.name}"
    def to_json(self):
        return self.__dict__ 
    def from_json(term_str):
        if not isinstance (term_str, dict):
            raise Exception ("Expected type dict")
        return Term(term_str['id'], term_str['name'])
    
from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
class TermForm(FlaskForm):
    name = StringField('Term Title', validators=[DataRequired()])