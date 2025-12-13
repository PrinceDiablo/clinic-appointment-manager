from flask import Flask
from flask_login import LoginManager
from app.config import Config

# Initialize login manager
login_manager = LoginManager()
login_manager.login_view = "auth.login"   # redirect if not logged in

@login_manager.user_loader
def load_user(user_id):

    from app.auth.models import User
    from app.db import fetchone

    row = fetchone("SELECT * FROM users WHERE id=%s", (int(user_id),))
    return User.from_row(row)


def create_app():
    app = Flask(__name__)

    # Load all configuration values
    app.config.from_object(Config)

    # Initialize login manager with this app instance
    login_manager.init_app(app)

    # Register blueprints
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)


    return app





