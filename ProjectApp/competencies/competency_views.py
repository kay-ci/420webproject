from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .competency import Competency, CompetencyForm
from ..dbmanager import get_db

bp = Blueprint("competency", __name__, url_prefix="/competencies")

@bp.route("/", methods = ["GET", "POST"])
def show_competencies():
    form = CompetencyForm()
    if request.method == "POST" and form.validate_on_submit():
        newCompetency = Competency(form.id.data, form.competency.data, form.competency_achievement.data, form.competency_type.data)
        try:
            get_db().add_competency(newCompetency)#will throw on duplicate
        except ValueError as e:
            flash(e)
    return render_template("competencies.html", competencies = get_db().get_competencies(), form = form)

@bp.route("/delete/<id>/")
def delete_competency(id):
    try:
        get_db().delete_competency(id)
    except ValueError:
        flash("couldn't find competency with this id to delete")
    return redirect(url_for("competency.show_competencies"))

@bp.route("/<id>/", methods = ["GET", "POST"])
def show_competency(id):
    form = CompetencyForm()
    if not isinstance(id, str):
        flash("could not find a competency with this id")
    competency = get_db().get_competency(id)
    if competency == None:
        flash("could not find a competency with this id")
        return redirect(url_for('competency.show_competencies')), 404
    if request.method == "POST" and form.validate_on_submit():
        get_db().update_competency(id, form.id.data, form.competency.data, form.competency_achievement.data, form.competency_type.data)
        competency = get_db().get_competency(form.id.data)
        return redirect(url_for("competency.show_competency", id = form.id.data))
    achievements = competency.competency_achievement.split("*")
    achievements.pop(0)
    return render_template("competency.html", competency = competency, form = form, achievements = achievements, elements = get_db().get_competency_elements(id))