from flask import render_template, redirect, url_for
from flask_login import current_user
from . import bp
from app.utils.navigation import landing_for_user

@bp.route('/')
def index():
    if current_user.is_authenticated:
        endpoint = landing_for_user(current_user)
        return redirect(url_for(endpoint))
    
    return render_template("main/index.html")
