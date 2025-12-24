from app.config import Config
from app.db import fetchone, get_db
from .seed_default_admin import seed_default_admin
from .seed_dev import seed_dev

def can_seed(): 
    """
    Returns True if no user exists in DB.
    """
    count = fetchone("SELECT COUNT(*) AS c FROM users")["c"]
    return count == 0

def run_seed_if_needed():
    if not can_seed():
        return # DB already initialized 
    
    db = get_db()

    try:
        # Transaction begins
        db.begin()

        # Create default admin
        seed_default_admin()
        
        # Dev-only seed
        if Config.FLASK_ENV == "development":
            seed_dev()
        
        # Commit if everything succeeds
        db.commit()
    
    except Exception:
        # Rollback on any failure
        db.rollback()
        raise

