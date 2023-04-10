class Competency:
    def __init__(self, id, competency, competency_achievement, competency_type):
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if len(str(id)) > 4:
            raise ValueError("id must not exceed 4 characters")
        if not isinstance(competency, str):
            raise TypeError("competency must be a string")
        if len(str(competency)) > 250:
            raise ValueError("competency must not exceed 250 characters")
        if not isinstance(competency_achievement, str):
            raise TypeError("competency achievement must be a string")
        if len(str(competency_achievement)) > 500:
            raise ValueError("competency achievement must not exceed 500 characters")
        if not isinstance(competency_type, str):
            raise TypeError("competency type must be a string")
        if len(str(competency_type)) > 10:
            raise ValueError("competency type must not exceed 10 characters")
        self.id = id
        self.competency = competency
        self.competency_achievement = competency_achievement
        self.competency_type = competency_type

    def __repr__(self):
        return f"Competency({self.id}, {self.competency}, {self.competency_achievement}, {self.competency_type})"
    def __str__(self):
        return f"Competency: {self.id}, {self.competency}, {self.competency_achievement}, {self.competency_type}"

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
    
class CompetencyForm(FlaskForm):
    id = StringField('competency id', validators=[DataRequired(), Length(max = 4)])
    competency = StringField('competency title', validators=[DataRequired(), Length(max = 250)])
    competency_achievement = TextAreaField('competency achievement', validators=[DataRequired(), Length(max = 500)])
    competency_type = SelectField('competency type', choices=[("mandatory"),("optional")], validators=[DataRequired()])