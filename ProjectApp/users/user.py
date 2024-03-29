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
        self.member_type = None
        
    def __repr__(self):
        return f'User({self.name}, {self.email})'
        
    def __str__(self):
        value = f'{self.name}: {self.email}'
        return value
    

from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import EmailField, PasswordField, StringField, BooleanField
from wtforms.validators import DataRequired,EqualTo, Regexp, Length

class SignupForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm  = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    name = StringField("Name", validators=[DataRequired(), Regexp("[A-Za-z]", message="Name must contain only letters"), Length(min=1)])
    avatar = FileField("Choose your own avatar!")

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    
class ProfileEdit(FlaskForm):
    name = StringField("Name:", validators=[DataRequired()])
    avatar_path = FileField("Select avatar")

class ChangePassword(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])