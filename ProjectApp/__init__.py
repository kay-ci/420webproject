import os
import secrets
from flask import Flask, render_template

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY=secrets.token_urlsafe(32),)
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    init_app(app)
    return app

def init_app(app):
    app.teardown_appcontext(cleanup)

    #from competencies.competency_views import bp as competency_bp
    #app.register_blueprint(competency_bp)
    #from courses.course_views import bp as course_bp
    #app.register_blueprint(course_bp)
    from domains.domain_views import bp as domain_bp
    app.register_blueprint(domain_bp)
    #from elements.element_views import bp as element_bp
    #app.register_blueprint(element_bp)
    #from terms.term_views import bp as term_bp
    #app.register_blueprint(term_bp)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404

def cleanup(value):
    pass