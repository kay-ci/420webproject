from flask import (Blueprint, render_template, 
                   url_for, redirect, abort, flash, request)
from ProjectApp.dbmanager import get_db
from ProjectApp.domains.domain import Domain, DomainForm
from datetime import datetime

bp = Blueprint('domains', __name__, url_prefix='/domains/')

@bp.route('/', methods=['GET', 'POST']) 
def show_domains():
    domains = get_db().get_domains()
    form = DomainForm()
    return render_template('domains.html',domains=domains)

@bp.route("<int:id>")
def show_domain(id, methods=["GET","POST"]):
    if not isinstance(id, int):
        abort(404)
    domain = get_db().get_domain(id)
    if domain == None:
        abort(404)
    form = DomainForm()
    if request.method == "POST":
        get_db().update_domain(domain)
    return render_template("domain.html", domain = domain, form = form, courses = get_db().get_domain_courses(id))

@bp.route("/delete/<int:id>")
def delete_domain(id):
    if not isinstance(id, int):
        flash("could not find domain with this id")
        return redirect(url_for('domains.show_domains'))
    domain = get_db().get_domain(id)
    if domain == None:
        flash("could not find domain with this id")
        return redirect(url_for('domains.show_domains'))
    get_db().delete_domain(id)
    return redirect(url_for('domains.show_domains'))