from flask import Flask
from flask_wtf import CSRFProtect
from flask_migrate import Migrate
from .extensions import db, login_manager
from app.utils.gravatar import gravatar_url

csrf = CSRFProtect()


def create_app():
    app = Flask(
        __name__,
        static_folder='../static',
        template_folder='../templates'
    )
    app.config.from_object("config.Config")

    # Init extensions
    csrf.init_app(app)
    db.init_app(app)

    app.jinja_env.filters['gravatar'] = gravatar_url

    # Import models here so Alembic sees them
    from . import models

    migrate = Migrate(app, db)
    login_manager.init_app(app)
    # TODO replace this with auth.login
    login_manager.login_view = "create.index"
    login_manager.login_message_category = "info"

    # Register blueprints
    from app.routes.home import home_bp
    from app.routes.create import create_bp
    from app.routes.auth import auth_bp
    from app.routes.edit import edit_bp
    from app.routes.profile import profile_bp
    from app.routes.view import view_bp
    from app.routes.api import api_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(create_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(edit_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(view_bp)
    app.register_blueprint(api_bp)

    return app
