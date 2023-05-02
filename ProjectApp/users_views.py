from flask import (Blueprint, render_template, 
                   url_for, redirect, abort, flash, request)

from ProjectApp.user import ChangePassword, ProfileEdit
from .dbmanager import get_db
from flask_login import current_user
from werkzeug.security import generate_password_hash


bp = Blueprint('users',__name__,url_prefix='/dashboard')

@bp.route('/')
def get_users():
    try:
        if not current_user.is_authenticated:
            flash("You are not a member.")
            return redirect(url_for('home.login_index'))
        else: 
            users = get_db().get_users()
    except Exception as e:
        users = None
        flash('Unable to connect with the database')
    if not users or len(users) == 0:
        abort(404)
    return render_template('admin_dash.html', users=users)

@bp.route('/promote/<string:email>/')
def promote_user(email):
    try:
        userChosen = get_db().get_user(email)
        get_db().promote_user(userChosen)
        users = get_db().get_users()
    except Exception as e:
        userChosen = None
        flash('Unable to promote that user, not found')
    return render_template('admin_dash.html', users=users)

@bp.route('/demote/<string:email>/')
def demote_user(email):
    try:
        userChosen = get_db().get_user(email)
        get_db().demote_user(userChosen)
        users = get_db().get_users()
    except Exception as e:
        userChosen = None
    return render_template('admin_dash.html', users=users)

@bp.route('/remove/<string:email>/')
def delete_user(email):
    try:
        userChosen = get_db().get_user(email)
        users = get_db().get_users()
        get_db().delete_user(userChosen)
    except Exception as e:
        userChosen = None
        flash('Unable to remove that user, not found')
    return render_template('admin_dash.html', users=users)

@bp.route('/edit/<string:email>', methods=['GET','POST'])
def edit_user(email):
    try:
        userChosen = get_db().get_user(email)
        form = ProfileEdit(email=userChosen.email,name=userChosen.name)
        if form.validate_on_submit():
            new_email = form.email.data
            name = form.name.data
            get_db().update_user_name(userChosen,name)
            get_db().update_user_email(userChosen,new_email)
            return redirect(url_for('users.get_users'))
        return render_template('editUser.html', form=form, userChosen=userChosen)
    except Exception as e:
        abort(404)
        
@bp.route('/edit/<string:email>/passwordchange/', methods=['GET','POST'])
def edit_user_password(email):
    try:
        userChosen = get_db().get_user(email)
        form = ChangePassword()
        if form.validate_on_submit():
            hash = generate_password_hash(form.password.data)
            get_db().update_user_password(userChosen,hash)
            return redirect(url_for('users.get_users'))
        return render_template('changePassword.html',form=form,userChosen=userChosen)
    except Exception as e:
        abort(404)

@bp.route('/blocked/<string:email>/')
def block_user(email):  
    try:
        userChosen = get_db().get_user(email)
        users = get_db().get_users()
        get_db().block_user(userChosen)
    except Exception as e:
        userChosen = None
        flash('Unable to block that user, not found')
    return render_template('admin_dash.html', users=users)   
