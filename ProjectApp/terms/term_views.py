from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .term import Term
from ..dbmanager import get_db

bp = Blueprint("term", __name__, url_prefix="/terms")

@bp.route("/")
def show_terms():
    return render_template("terms.html", terms = get_db().get_terms())

@bp.route("/<int:id>/")
def show_term(id):
    if not isinstance(id, int):
        flash("could not find a term with this id")
    term = get_db().get_term(id)
    if term == None:
        flash("could not find a term with this id")
        return redirect(url_for('term.show_terms')), 404
    return render_template("term.html", term = term)