from flask import abort

def landing_for_user(user):
    if user.has_role("admin"):
        return "admin.dashboard"

    if user.has_role("doctor"):
        return "doctor.dashboard"

    if user.has_role("clinic_receptionist"):
        return "receptionist.dashboard"

    if user.has_role("patient"):
        return "patient.dashboard"

    abort(403)
