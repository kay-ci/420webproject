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

@bp.route("/<int:id>/", methods = ["GET", "POST"])
def show_term(id):
    form = TermForm()
    if request.method == "POST" and form.validate_on_submit():
        try:
            name = str.lower(form.name.data)
            if(valid_name(name)):
                get_db().update_term(Term(id, name))
                flash("Term updated succefully!")
                return redirect(url_for("term.show_term", id = id))
            else:
                flash("Term name must be Fall, Winter or Summer")
        except:
            flash("Could not update Term")
   
    try:
        term = get_db().get_term(int(id))
        courses = get_db().get_term_courses(int(id))  
        return render_template("term.html", term = term, courses = courses, form = form)
    except:
        if term == None:
            flash("could not find a term with this id")
            abort(404)
    
            

@bp.route("/add/", methods = ["GET", "POST"]) 
def add_term():
    form = TermForm()
    if request.method == "POST" and form.validate_on_submit():
        name = str.lower(form.name.data)
        if (valid_name(name)):
            try:
                term = Term(None, name)
                get_db().add_term(term)
                msg = f'{str.capitalize(term.name)} Term added succesfully!'
                flash(msg)
                return redirect(url_for("term.show_terms"))
            except Exception as e:
                flash("A term with that Id already exists")
                flash(str(e))
        else:
            flash("term should be titled, winter, fall or summer")
    return render_template("add_term.html", form = form) 

@bp.route("/delete/<id>/")
def delete_term(id):
    try:
        get_db().delete_term(int(id))
        msg = f'Deleted Term {id}'
        flash(msg)
    except Exception as e:
        flash("Could not delete term")
    return redirect(url_for("term.show_terms"))

def valid_name(name):
    if (name == "winter" or name == "fall" or name == "summer"):
        return True
    return  False  
