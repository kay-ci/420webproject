from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .competency import Competency, CompetencyForm, CompleteCompetencyForm
from ..elements.element import ElementForm, Element
from ..dbmanager import get_db

bp = Blueprint("competency", __name__, url_prefix="/competencies")

@bp.route("/")
def show_competencies():
    try:
        competencies = get_db().get_competencies()
    except:
        flash("Could not load competencies")
        abort(404)
    return render_template("competencies.html", competencies = competencies)

@bp.route("/add/", methods = ["GET", "POST"])#login required
def add_competency():
    form = CompleteCompetencyForm()
    if request.method == "POST" and form.validate_on_submit():
        competency = Competency(form.competency_id.data, form.competency.data, form.competency_achievement.data, form.competency_type.data)
        if get_db().get_competency(form.competency_id.data) != None:
            flash("this competency id is already being used")
            return render_template("add_competency.html", form = form)
        get_db().add_competency(competency)
        element = Element(None, get_db().get_next_competency_element_order(form.competency_id.data), form.element.data, form.element_criteria.data, form.competency_id.data)
        get_db().add_element(element)
        return redirect(url_for('competency.show_competency', id = competency.id))
    return render_template("add_competency.html", form = form)
        
            

@bp.route("/delete/<id>/")
def delete_competency(id):
    try:
        get_db().delete_competency(id)
    except ValueError:
        flash("couldn't find competency with this id to delete")
        abort(404)
    return redirect(url_for("competency.show_competencies"))

@bp.route("/<id>/", methods = ["GET", "POST"])
def show_competency(id):
    competency_form = CompetencyForm()
    element_form = ElementForm()
    if not isinstance(id, str):
        flash("could not find a competency with this id")
    competency = get_db().get_competency(id)
    if competency == None:
        flash("could not find a competency with this id")
        return redirect(url_for('competency.show_competencies')), 404
    if request.method == "POST":
        if element_form.element.data == None:#if true then its the competency form that was submitted
            competency_form.validate_on_submit()#what does validate_on_submit even do?
            get_db().update_competency(id, competency_form.competency.data, competency_form.competency_achievement.data, competency_form.competency_type.data)
        else:# means the submitted form is element
            element = Element(None, get_db().get_next_competency_element_order(id), element_form.element.data, element_form.element_criteria.data, id)
            get_db().add_element(element)
        return redirect(url_for("competency.show_competency", id = id))
    achievements = competency.competency_achievement.split("*")
    if len(achievements) != 1:
        achievements.pop(0)
    return render_template("competency.html", competency = competency, competency_form = competency_form, element_form = element_form, achievements = achievements, elements = get_db().get_competency_elements(id))