from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from . import bp
from app.utils.permissions import permissions_required
from .service import create_user_by_staff, list_users_for, assign_role_to, remove_role_of

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

@bp.route("/list_users", methods=["GET"])
@login_required
@permissions_required("manage_users")
def list_users():

    data = list_users_for(current_user)
    return render_template("users/list.html", **data)

@bp.route("/assign_role", methods=["POST"])
@login_required
@permissions_required("manage_users")
def assign_role():
    try:
        target_user_id = assign_role_to(current_user, request.form)
    except ValueError as e:
        flash (str(e))
        return redirect(url_for("users.list_users"))

    flash("Role successfully assigned", "success")
    return redirect(url_for("users.list_users"))

@bp.route("/remove_role", methods=["POST"])
@login_required
@permissions_required("manage_users")
def remove_role():
    try:
        target_user_id = remove_role_of(current_user, request.form)
    except ValueError as e:
        flash (str(e))
        return redirect(url_for("users.list_users"))

    flash("Role successfully removed", "success")
    return redirect(url_for("users.list_users"))