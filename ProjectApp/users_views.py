from flask import (Blueprint, render_template, 
                   url_for, redirect, abort, flash, request)
from .dbmanager import get_db


bp = Blueprint('users',__name__,url_prefix='/dashboard')

@bp.route('/')
def get_users():
    try:
        users = get_db().get_users()
    except Exception as e:
        users = None
        flash('Unable to connect with the database')
    if not users or len(users) == 0:
        abort(404)
    return render_template('admin_dash.html', users=users)

@bp.route('/promote/')
def promote_user(email):
    try:
        userChosen = get_db().get_user(email)
        get_db().promote_user(userChosen)
    except Exception as e:
        userChosen = None
        flash('Unable to promote that user, not found')
    return render_template('admin_dash.html',userChosen=userChosen)

@bp.route('/demote/')
def demote_user(email):
    try:
        userChosen = get_db().get_user(email)
        get_db().demote_user(userChosen)
    except Exception as e:
        userChosen = None
        flash('Unable to demote that user, not found')
    return render_template('admin_dash.html',userChosen=userChosen)
    