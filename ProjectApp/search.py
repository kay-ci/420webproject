class Search:
    def __init__(self, category, word):
        
        if not isinstance(category, str):
            raise Exception("category must be a string")
        if not isinstance(word, str):
            raise Exception("word to match must be a string")

        self.word = word
        self.category = category
    
    def __repr__(self):
        return f'Search({self.word}, {self.category})'
        
    def __str__(self):
        value = f'{self.word}, {self.category}'
        return value
    
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
    
class SearchForm(FlaskForm):
    word = StringField('Words to match', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])