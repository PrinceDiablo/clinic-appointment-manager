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

    row = fetchone(
        """
        SELECT 
            u.*,
            GROUP_CONCAT(DISTINCT r.name ORDER BY r.name) AS roles,
            GROUP_CONCAT(DISTINCT p.name ORDER BY p.name) AS permissions 
        FROM users u 
        JOIN user_roles ur ON ur.user_id = u.id
        JOIN roles r ON r.id = ur.role_id
        JOIN role_permissions rp ON rp.role_id = r.id
        JOIN permissions p ON p.id = rp.permission_id
        WHERE u.id = %s AND u.is_active = 1
        GROUP BY u.id;
        """, (int(user_id),))
    if not row:
        return None
    
    roles = row["roles"].split(",") if row["roles"] else []
    permissions = row["permissions"].split(",") if row["permissions"] else []

    return User.from_row(row, roles, permissions)


def create_app():
    app = Flask(__name__)

    # Load all configuration values
    app.config.from_object(Config)

    # Initialize login manager with this app instance
    login_manager.init_app(app)

    # Register blueprints
    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .appointments import bp as appt_bp
    app.register_blueprint(appt_bp)

    from .users import bp as users_bp
    app.register_blueprint(users_bp)

    from .dashboards.main import bp as main_bp
    app.register_blueprint(main_bp)

    from .dashboards.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from .dashboards.doctor import bp as doc_bp
    app.register_blueprint(doc_bp)

    from .dashboards.clinic_receptionist import bp as recpt_bp
    app.register_blueprint(recpt_bp)

    from .dashboards.patient import bp as patient_bp
    app.register_blueprint(patient_bp)

    # Seed DB with data on first initialization
    from app.seed import run_seed_if_needed
    with app.app_context():
        run_seed_if_needed()

    #Ensure DB connection is closed after each request
    from app.db import close_db
    app.teardown_appcontext(close_db)

    return app
