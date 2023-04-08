from flask import Blueprint, render_template, request, redirect, url_for, flash
from .competency import Competency, CompetencyForm
from ..dbmanager import get_db

bp = Blueprint("competency", __name__, url_prefix="/competencies")

@bp.route("/", methods = ["GET", "POST"])
def list_competencies():
    form = CompetencyForm()
    if request.method == "POST" and form.validate_on_submit():
        newCompetency = Competency(form.id.data, form.competency.data, form.competency_achievement.data, form.competency_type.data)
        try:
            get_db().add_competency(newCompetency)#will throw on duplicate
        except ValueError as e:
            flash(e)
    return render_template("competencies.html", competencies = get_db().get_competencies(), form = form)

@bp.route("/delete/<id>")
def delete_competency(id):
    get_db().delete_competency(id)
    return redirect(url_for("competency.list_competencies"))