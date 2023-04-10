from flask import (Blueprint, render_template, 
                   url_for, redirect, abort, flash, request)
from dbmanager import get_db
from domain import Domain
from datetime import datetime

bp = Blueprint('posts', __name__, url_prefix='/domains/')

@bp.route('/')
def get_domains():
    try:
        domains = get_db().get_domains()
    except Exception as e:
        domains = None
        flash('Unable to connect with the database')
    if not domains or len(domains) == 0:
        abort(404)
    return render_template('domains.html', domains=domains)







