from flask import (Blueprint, render_template, 
                   url_for, redirect, abort, flash, request)
from ProjectApp.dbmanager import get_db
from ProjectApp.domains.domain import Domain, DomainForm
from datetime import datetime

bp = Blueprint('domain_views', __name__, url_prefix='/domains/')

@bp.route('/', methods=['GET', 'POST']) 
def get_domains():
    domains = get_db().get_domains()
    alreadyADomain = False
    if len(domains) == 0:
        abort(404)
    form = DomainForm()
    if request.method == 'POST' and form.validate_on_submit():
        domain = Domain(form.id.data, form.domain.data, form.description.data)
        try:
            get_db().insert_domain(domain)
            return redirect(url_for('domain_views.get_domains'))
        except ValueError as e:
            flash(str(e))
    return render_template('domains.html',domains=domains, form=form)







