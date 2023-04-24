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
    