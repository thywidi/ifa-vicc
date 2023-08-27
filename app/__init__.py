from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_required
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_object(Config)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    @app.route("/index")
    @login_required
    def home():
        return render_template(
            "pages/index.html",
            title="Home",
        )

    return app


from app import models  # noqa: E402, F401
