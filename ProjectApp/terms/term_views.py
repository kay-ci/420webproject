from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .term import Term, TermForm
from ..dbmanager import get_db

bp = Blueprint("term", __name__, url_prefix="/terms")

# post a new term
@bp.route("/")
def show_terms():
    try:
        terms = get_db().get_terms()
    except:
        flash("Could not load terms")
        abort(404)
    return render_template("terms.html", terms = terms)


@bp.route("/add/", methods = ["GET", "POST"]) 
def add_term():
    form = TermForm()
    if request.method == "POST" and form.validate_on_submit():
        name = str.lower(form.name.data)
        id = form.id.data
        if (name == "winter" or name == "fall" or name == "summer"):
            term = Term(int(id), name)
            get_db().add_term(term)
            return redirect(url_for("term.show_term", id = id))
        else:
            flash("term should be titled, winter, fall or summer")
            

@bp.route("/<int:id>/")
def show_term(id):
    if not isinstance(id, int):
        flash("could not find a term with this id")
    term = get_db().get_term(id)
    if term == None:
        flash("could not find a term with this id")
        return redirect(url_for('term.show_terms')), 404
    return render_template("term.html", term = term, courses = get_db().get_term_courses(id))
