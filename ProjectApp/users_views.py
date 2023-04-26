from flask import (Blueprint, render_template, 
                   url_for, redirect, abort, flash, request)

from ProjectApp.user import ProfileEdit
from .dbmanager import get_db
from flask_login import current_user


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
        flash('Unable to demote that user, not found')
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

@bp.route('/edit/<string:email>')
def edit_user(email):
    try:
        form = ProfileEdit()
        userChosen = get_db().get_user(email)
        return render_template('editUser.html', form=form, userChosen=userChosen)
    except Exception as e:
        abort(404)
    