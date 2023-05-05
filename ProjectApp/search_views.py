import os
from flask import Blueprint, current_app, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.security import generate_password_hash

from ProjectApp.search import SearchForm
from .dbmanager import get_db

bp = Blueprint("search",__name__,url_prefix='/search/')

@bp.route('/', methods=['POST','GET'])
def show_search():
    form = SearchForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            match = form.word.data
            category = form.category.data
            if category == 'domains':
                domains = get_db().search_domains(match)
                if len(domains) == 0:
                    flash('No matches found.')
                    return render_template('search.html', form=form)
                return render_template('search.html',form=form,domains=domains)
            elif category == 'terms':
                terms = get_db().search_terms(match)
                if len(terms) == 0:
                    flash('No matches found.')
                    return render_template('search.html', form=form)
                return render_template('search.html',form=form,terms=terms)
            elif category == 'courses':
                courses = get_db().search_courses(match)
                if len(courses) == 0:
                    flash('No matches found.')
                    return render_template('search.html', form=form)
                return render_template('search.html',form=form,courses=courses)
            elif category == 'competencies':
                competencies = get_db().search_competencies(match)
                if len(competencies) == 0:
                    flash('No matches found.')
                    return render_template('search.html', form=form)
                return render_template('search.html',form=form,competencies=competencies)
            else:
                flash('Category not found.')
    return render_template('search.html', form=form)