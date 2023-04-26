from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from .element import Element, ElementForm
from ..dbmanager import get_db
bp = Blueprint("element", __name__, url_prefix='/elements')

@bp.route("/", methods = ["GET", "POST"])
def show_elements():
    form = ElementForm()
    # ask teammates about what to make of new_element since element_orde and competency_id are no longers forms
    if request.method == "POST" and form.validate_on_submit():
        new_element = Element(None, form.element_order.data, form.element.data, form.element_criteria.data, form.competency_id.data)
        try:
            get_db().add_element(new_element)
        except ValueError as e:
            flash(e)
    return render_template("elements.html", elements = get_db().get_elements(), form = form)

@bp.route("/<element_id>")
def show_element(element_id):
    form = ElementForm()
    try:
        element = get_db().get_element(int(element_id))
    except Exception:
        element = None
        abort(404)
    return render_template("element.html", element = element, form = form)

@bp.route("/delete/<element_id>/")
def delete_element(element_id):
    try:
        get_db().delete_element(element_id)
        message = f'deleted element with id {element_id}'
        flash(message)
    except ValueError as e:
        flash(str(e))#there can be many reasons for this: element id doesnt exist or its the last of its competency
    return redirect(url_for("element.show_elements"))