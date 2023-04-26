import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.security import generate_password_hash
from .dbmanager import get_db
from .user import SignupForm, User
from flask_login import login_user, logout_user

bp = Blueprint("auth", __name__, url_prefix='/auth/')

@bp.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.avatar.data
            avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], 
                                       form.email.data)
            if not os.path.exists(avatar_dir):
                os.makedirs(avatar_dir)
            avatar_path = os.path.join(avatar_dir, 'avatar.png')
            if file != None:
                file.save(avatar_path)
                #what should we do if user doesn't give a file for avatar
            hash = generate_password_hash(form.password.data)
            user = User(form.email.data, hash, form.name.data)
            get_db().insert_user(user)
            userInserted = get_db().get_user(form.email.data)
            login_user(userInserted)
            return redirect(url_for('courses.list_courses'))
    return render_template('signup.html', form=form)

@bp.route('/logout/')
#@login_required
def logout():
    logout_user()
    return render_template('logout.html')

@bp.route('/avatar/<email>/avatar.png')
def get_avatar(email):
    avatar_dir = os.path.join(current_app.config['IMAGE_PATH'], email)
    return send_from_directory(avatar_dir, 'avatar.png')
