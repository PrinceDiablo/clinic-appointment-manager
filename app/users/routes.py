from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from . import bp
from app.utils.permissions import permissions_required
from .service import create_user_by_staff

@bp.route("/create_user", methods=["GET","POST"])
@login_required
@permissions_required("create_user")
def create_user():

    if request.method == "GET":
        return render_template("users/create.html")
    
    try:
        user_id = create_user_by_staff(current_user, request.form)
    except ValueError as e:
        flash (str(e))
        return redirect(url_for("users.create_user"))
    
    flash("User created successfully", "success")
    return redirect(url_for("appointments.create_appointment"))
