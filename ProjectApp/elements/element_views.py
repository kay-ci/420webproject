from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .element import Element, ElementForm
from ..dbmanager import get_db
bp = Blueprint("element", __name__, url_prefix='elements')

@bp.route("/", methods = ["GET", "POST"])
def show_elements():
    form = ElementForm()
    if request.method == "POST" and form.validate_on_submit():
        new_element = Element(form.element_id.data, form.element_order.data, form.element.data, form.element_criteria.data, form.competency_id.data)
        try:
            get_db().add_element(new_element)
        except ValueError as e:
            flash(e)
    return render_template("elements.html", elements = get_db().get_elements(), form = form)

@bp.route("/<element_id>", methods = ["GET", "POST"])
def show_element(element_id):
    form = ElementForm()
    element = get_db().get_element(int(element_id))
    if element == None:
        flash("Element with that id not found")
        abort(404)
    if request.method == "POST" and form.validate_on_submit():
        get_db().update_element(element_id, form.element_order.data, form.element.data, form.element_criteria.data, form.competency_id.data)
        element = get_db().get_element(form.element_id.data)
        return redirect(url_for("element.show_element", element_id = form.element_id.data))
    return render_template("element.html", element = element, form = form)

@bp.route("/delete/<element_id>/")
def delete_competency(element_id):
    try:
        get_db().delete_element(element_id)
    except ValueError:
        flash("couldn't find element with this id to delete")
    return redirect(url_for("element.show_elements"))