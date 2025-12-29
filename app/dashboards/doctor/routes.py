from flask import render_template
from flask_login import login_required
from . import bp
from app.utils.permissions import permissions_required


@bp.route('/dashboard')
@login_required
@permissions_required('view_doctors')
def dashboard():
    return render_template("doctor/dashboard.html")