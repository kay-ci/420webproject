class Term:
    def __init__(self, id, name):
        if not isinstance(id, int):
            raise TypeError("expecting an id of type int")
        if not isinstance(name, str):
            raise TypeError("expecting a name of type str")
        if id <= 0:
            raise ValueError("id must be positive")
        if len(name) > 6:
            raise ValueError("name must not exceed 6 characters")
        if not name:
            raise ValueError("name can not be null")
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
        return Term(None, term_str['name'])
    
from flask_wtf import FlaskForm 
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
class TermForm(FlaskForm):
    id = IntegerField('Term_Id', validators=[DataRequired()])
    name = StringField('Term Title', validators=[DataRequired()])