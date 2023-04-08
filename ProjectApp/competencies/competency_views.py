from flask import Blueprint, render_template
from .competency import Competency, CompetencyForm
from ..dbmanager import get_db

bp = Blueprint("competency", __name__, url_prefix="/competencies")

@bp.route("/", methods = ["GET", "POST"])
def list_competencies():
    form = CompetencyForm()
    competencies = get_db().get_competencies()
    return render_template("competencies.html", competencies = competencies, form = form)