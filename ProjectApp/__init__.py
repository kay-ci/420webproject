import os
import secrets
from flask import Flask, render_template
from .dbmanager import get_db
from flask_login import LoginManager
from .dbmanager import close_db

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secrets.token_urlsafe(32),
        IMAGE_PATH=os.path.join(app.instance_path, 'images')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    init_app(app)
    
    from .home.home_views import bp as home_bp
    app.register_blueprint(home_bp)

    from .competencies.competency_views import bp as competency_bp
    app.register_blueprint(competency_bp)
    
    from .competencies.competencies_api import bp as competencies_api_bp
    app.register_blueprint(competencies_api_bp)
    
    from .courses.course_views import bp as course_bp
    app.register_blueprint(course_bp)
    
    from .courses.courses_api import bp as courses_api
    app.register_blueprint(courses_api)
    
    from .courses.courses_elements_views import bp as courses_elements_bp
    app.register_blueprint(courses_elements_bp)
    
    from .courses.courses_elements_api import bp as courses_elements_api_bp
    app.register_blueprint(courses_elements_api_bp)
 
    from .domains.domain_views import bp as domain_bp
    app.register_blueprint(domain_bp)
    
    from .domains.domains_api import bp as domain_bp_api
    app.register_blueprint(domain_bp_api)
    
    from .terms.term_views import bp as term_bp
    app.register_blueprint(term_bp)
    
    from .terms.terms_api import bp as api_term_bp
    app.register_blueprint(api_term_bp)
    
    from .auth_views import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .users.users_views import bp as users_bp
    app.register_blueprint(users_bp)
    
    from .elements.elements_api import bp as elements_api_bp
    app.register_blueprint(elements_api_bp)
    
    from .elements.element_views import bp as elem_bp
    app.register_blueprint(elem_bp)
    
    from .search_views import bp as search_bp
    app.register_blueprint(search_bp)
    
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'), 404
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.logout'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return get_db().get_user_id(int(user_id))

    os.makedirs(app.config['IMAGE_PATH'], exist_ok=True)

    return app
    
def init_app(app):
    app.teardown_appcontext(cleanup)

def cleanup(value):
    pass
