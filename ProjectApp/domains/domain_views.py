from flask import (Blueprint, render_template, 
                   url_for, redirect, abort, flash, request)
from ProjectApp.dbmanager import get_db
from ProjectApp.domains.domain import Domain, DomainForm
from datetime import datetime

bp = Blueprint('domain_views', __name__, url_prefix='/domains/')

@bp.route('/', methods=['GET', 'POST']) 
def get_domains():
    try:
        domains = get_db().get_domains()
    except Exception as e:
        domains = None
        flash("Could not load domains")
        flash(str(e))
        abort(404)
    alreadyADomain = False
    if len(domains) == 0:
        abort(404)
    form = DomainForm()
    if request.method == 'POST' and form.validate_on_submit():
        domain = Domain(form.id.data, form.domain.data, form.description.data)
        domainGot = domain
        for domain in domains:
            if domain.domain == domainGot.domain:
                alreadyADomain = True
        if alreadyADomain == False:
            domains.append(get_db().insert_domain(domainGot))
        else:
            flash("That domain Already exist")
    return render_template('domains.html',domains=domains, form=form)







