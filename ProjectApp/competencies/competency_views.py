from flask import Blueprint, render_template, request, redirect, url_for
from .competency import Competency, CompetencyForm
from ..dbmanager import get_db

bp = Blueprint("competency", __name__, url_prefix="/competencies")

@bp.route("/", methods = ["GET", "POST"])
def list_competencies():
    form = CompetencyForm()
    competencies = get_db().get_competencies()
    if request.method == "POST" and form.validate_on_submit():
        newCompetency = Competency(form.id.data, form.competency.data, form.competency_achievement.data, form.competency_type.data)
        try:
            get_db().get_competency(form.id.data)
        except ValueError:
            get_db().add_competency(newCompetency)
    return render_template("competencies.html", competencies = competencies, form = form)

@bp.route("/delete/<id>")
def delete_competency(id):
    get_db().delete_competency(id)
    return redirect(url_for("competency.list_competencies"))