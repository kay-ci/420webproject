from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user
from ProjectApp.dbmanager import get_db
from werkzeug.security import check_password_hash

from ProjectApp.user import LoginForm

bp = Blueprint('home', __name__, url_prefix="/")


@bp.route('/login/', methods=['GET', 'POST'])
def login_index():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            user = get_db().get_user(email)
            if user:
                # Check password
                pwd = form.password.data
                if check_password_hash(user.password, pwd):
                    login_user(user, remember=form.remember_me.data)
                else:
                    flash("Invalid information")
            else:
                flash("Could not find user")
                redirect(url_for('auth.signup'))
        else:
            flash("Invalid form")
    return render_template('index.html', form=form)


