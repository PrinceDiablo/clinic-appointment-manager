from functools import wraps
from flask import abort
from flask_login import current_user

def permissions_required(*permissions):
    def decorator(fn):
        required = set(p.lower() for p in permissions)
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if not any(permission in current_user.permissions for permission in required):
                abort(403)
            return fn(*args, **kwargs)
        return wrapper
    return decorator