from flask_login import UserMixin
class User(UserMixin):
    def __init__(self, email, password, name):
        if not isinstance(email, str):
            raise TypeError()
        if not isinstance(password, str):
            raise TypeError()
        if not isinstance(name, str):
            raise TypeError()
        self.email = email
        self.name=name
        self.password = password
        self.id = None

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
