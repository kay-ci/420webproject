class Domain:
    def __init__(self, domain_id, domain, domain_description):
        
        if not(domain_id == None or isinstance(domain_id, int)):
            raise Exception("domain id must be a number")
        if not isinstance(domain, str):
            raise Exception("domain must be a string")
        if not isinstance(domain_description, str):
            raise Exception("domain description must be a string")

        self.domain_id = domain_id
        self.domain = domain
        self.domain_description = domain_description
    
    def __repr__(self):
        return f'Domain({self.domain_id}, {self.domain}, {self.domain_description})'
        
    def __str__(self):
        value = f'{self.domain_id}: {self.domain}, {self.domain_description}'
        return value
    
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
    
class DomainForm(FlaskForm):
    domain = StringField('Name', validators=[DataRequired()])
    domain_description = StringField('Description', validators=[DataRequired()])


