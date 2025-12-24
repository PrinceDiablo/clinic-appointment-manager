from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not any(role in roles for role in current_user.roles):
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator