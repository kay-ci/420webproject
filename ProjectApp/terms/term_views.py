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

@bp.route("/<int:id>/")
def show_term(id):
    try:
        term = get_db().get_term(int(id))
        courses = get_db().get_term_courses(int(id))
        return render_template("term.html", term = term, courses = courses)
    except:
        if term == None:
            flash("could not find a term with this id")
            abort(404)

@bp.route("/add/", methods = ["GET", "POST"]) 
def add_term():
    form = TermForm()
    if request.method == "POST" and form.validate_on_submit():
        name = str.lower(form.name.data)
        id = form.id.data
        if (name == "winter" or name == "fall" or name == "summer"):
            try:
                term = Term(int(id), name)
                get_db().add_term(term)
                flash("Term added succesfully!")
                return redirect(url_for("term.show_term", id = id))
            except Exception as e:
                flash("A term with that Id already exists")
                flash(str(e))
        else:
            flash("term should be titled, winter, fall or summer")
    return render_template("add_term.html", form = form) 

@bp.route("/delete/<id>/")
def delete_term(id):
    try:
        get_db().delete_term(id)
    except:
        flash("Could not delete term")
    return redirect(url_for("term.show_terms"))
