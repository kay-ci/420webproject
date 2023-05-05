from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .element import Element, ElementForm
from ..dbmanager import get_db
bp = Blueprint("element", __name__, url_prefix='/elements')

@bp.route("/", methods = ["GET", "POST"])
def show_elements():
    return redirect(url_for("competency.show_competencies"))

@bp.route("/<int:element_id>", methods = ["GET", "POST"])
def show_element(element_id):
    form = ElementForm()
    try:
        element = get_db().get_element(int(element_id))
    except Exception:
        element = None
        abort(404)
    if request.method == "POST":
        if form.validate_on_submit():
            try:
                new_element = Element(int(element_id), int(element.element_order), form.element.data, form.element_criteria.data, element.competency_id)
                get_db().update_element(new_element)
                flash("Element updated succesfully")
                return redirect(url_for("element.show_element", element_id = new_element.element_id))
            except Exception as e:
                flash("Something went wrong could not update")
                flash(str(e))
        else: 
            flash("invalid form")
    return render_template("element.html", element = element, form = form)

@bp.route("/delete/<element_id>/")
def delete_element(element_id):
    try:
        element = get_db().get_element(int(element_id))
        if element == None:
            flash("element not found")
            abort(404)
        get_db().delete_element(element_id)
        message = f'deleted element with id {element_id}'
        flash(message)
    except ValueError as e:
        flash(str(e))#there can be many reasons for this: element id doesnt exist or its the last of its competency
    return redirect(url_for("competency.show_competency", id = element.competency_id))