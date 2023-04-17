from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, password, name):
        if not isinstance(email, str):
            raise Exception('Email must be a string')
        if not isinstance(password, str):
            raise TypeError('Password must be a string')
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        self.email = email
        self.name= name
        self.password = password
        self.id = None
        
    def __repr__(self):
        return f'User({self.name}, {self.email})'
        
    def __str__(self):
        value = f'{self.name}: {self.email}'
        return value
    

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    avatar = FileField("Choose your own avatar!")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me", validators=[DataRequired()])
