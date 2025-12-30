from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from . import bp
from app.utils.permissions import permissions_required
from app.appointments.service import list_appointments_for, create_appointment_for, update_appointment_status_for

@bp.route("/list", methods=["GET"])
@login_required
@permissions_required("view_appointments")
def list_appointments():
    """
    List appointments visible to the current user.
    Access is enforced via permission checks.
    Data scope is enforced in the service layer.
    """
    appointments = list_appointments_for(current_user)
    return render_template("appointments/list.html",appointments=appointments)

@bp.route("/create", methods=["GET", "POST"])
@login_required
@permissions_required("create_appointments")
def create_appointment():

    if request.method == "GET":
        return render_template("appointments/create.html")

    try:
        appointment_id = create_appointment_for(current_user, request.form)
    except ValueError as e:
        flash (str(e))
        return redirect(url_for("appointments.create_appointment")) 
    
    flash("Appointment created successfully", "success")
    return redirect(url_for("appointments.list_appointments"))

@bp.route("/update_status", methods=["POST"])
@login_required
@permissions_required("update_appointments")
def update_appointment_status():
    try:
        appointment_id = update_appointment_status_for(current_user, request.form)
    except ValueError as e:
        flash (str(e))
        return redirect(url_for("appointments.list_appointments"))
    
    flash("Appointment status updated successfully", "success")
    return redirect(url_for("appointments.list_appointments"))