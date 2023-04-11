from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, password, name, avatar_path):
        if not isinstance(email, str):
            raise Exception('Email must be a string')
        if not isinstance(password, str):
            raise TypeError('Password must be a string')
        if not isinstance(name, str):
            raise TypeError('Name must be a string')
        if not isinstance(avatar_path, str):
            raise TypeError('Avatar path must be as string')
        self.avatar_path = avatar_path
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
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    name = StringField("name", validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = EmailField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me", validators=[DataRequired()])
