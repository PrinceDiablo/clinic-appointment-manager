"""
Appointment domain service.

This module implements all appointment-related business logic, including:
- visibility rules for appointment listings
- creation of appointments with validation
- controlled status transitions using RBAC and ownership checks

Security model:
- Routes must enforce authentication and coarse permissions.
- This service layer enforces authorization, data scope,
  and valid state transitions.
"""

from app.db import fetchall, fetchone, execute, transaction
from datetime import datetime
from users.service import create_user_by_staff

ALLOWED_STATUSES = {
    "requested",
    "confirmed",
    "cancelled",
    "completed",
    "no_show"
}

VALID_TRANSITIONS = {
    "requested": {"confirmed", "cancelled"},
    "confirmed": {"completed", "cancelled", "no_show"}
}

def list_appointments_for(user) -> list[dict]:
    """
    Return appointment records visible to the given user.

    Security model:
    - Route must enforce authentication and basic permission checks.
    - Service enforces ownership and role-based authority.

    Authorization rules:
    - manage_appointments: full view with doctor and patient context
    - Clinic receptionist: operational view based on role
    - Doctor: own appointments with patient name
    - Patient: own appointments with doctor name
    - Others: empty list
    """
    # Full view: manage_appointments 
    if user.has_permission("manage_appointments"):
        return fetchall(
            """
            SELECT a.id, a.patient_id, a.doctor_id, a.appointment_timestamp, 
                a.arrival_timestamp, a.status, a.notes, a.created_by_staff, 
                a.deleted_at, a.created_at, a.updated_at, 
                d.name AS doctor_name, 
                p.name AS patient_name
            FROM appointments a
            JOIN user_details d ON a.doctor_id = d.user_id
            JOIN user_details p ON a.patient_id = p.user_id
            WHERE a.deleted_at IS NULL
            ORDER BY a.appointment_timestamp DESC 
            """
        )
    
    # Special view: Clinic_receptionist 
    if user.has_role("clinic_receptionist"):
        return fetchall(
            """
            SELECT a.id, a.appointment_timestamp, 
            a.arrival_timestamp, a.status, a.notes, 
            a.created_at, 
            d.name AS doctor_name, 
            p.name AS patient_name
        FROM appointments a
        JOIN user_details d ON a.doctor_id = d.user_id
        JOIN user_details p ON a.patient_id = p.user_id
        WHERE a.deleted_at IS NULL
        ORDER BY a.appointment_timestamp DESC 
            """ 
        )
        
    # Read-only access with scoped view
    if user.has_permission("view_appointments"):
        if user.has_role("doctor"):
            return fetchall(
                """
                SELECT a.id, a.appointment_timestamp, a.status,
                       p.name AS patient_name
                FROM appointments a
                JOIN user_details p ON a.patient_id = p.user_id
                WHERE a.doctor_id = %s AND a.deleted_at IS NULL
                ORDER BY a.appointment_timestamp DESC
                """, 
                (user.id,)
            )
        
        if user.has_role("patient"):
            return fetchall(
                """
                SELECT a.id, a.appointment_timestamp, a.status,
                       d.name AS doctor_name
                FROM appointments a
                JOIN user_details d ON a.doctor_id = d.user_id
                WHERE a.patient_id = %s AND a.deleted_at IS NULL
                ORDER BY a.appointment_timestamp DESC
                """, 
                (user.id,)
            )
        
        # Other roles with view_appointments but no scope
        return []
    
     # User has no permission at all
    return []

def create_appointment_for(user, data: dict) -> int:
    """
    Create a new appointment if the user is authorized.

    Security model:
    - Route must enforce authentication and basic permission checks.
    - Service enforces ownership and role-based authority.

    Authorization rules:
    - manage_appointments: can create appointments for any patient.
    - patient: can create appointments only for themselves.
    - Others: cannot create appointments.

    Data integrity:
    - DB INSERT are atomic.

    Raises:
        ValueError if validation or authorization is invalid.
    
    Returns:
        appointment_id(int)
    """
    # Extract and validate appointment data
    patient_id = data.get("patient_id")
    doctor_id = data.get("doctor_id")
    appt_date = data.get("appt_date")
    appt_time = data.get("appt_time")
    notes = data.get("notes")

    if not doctor_id or not appt_date or not appt_time:
        raise ValueError("Missing required appointment data")
    
    # Patient resolution
    if patient_id:
        try:
            patient_id = int(patient_id)
        except (TypeError, ValueError):
            raise ValueError("Invalid patient ID")   
    else: 
        if user.has_permission("create_user"):
            patient_id = create_user_by_staff(user, data)    
        else:
            raise ValueError("Patient must exist or user creation permission required")
    
    # Validate doctor
    try:
        doctor_id = int(doctor_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid doctor ID")
    
    # Role check
    if not _user_has_role(patient_id, "patient"):
        raise ValueError("Selected patient is not a valid patient.")
    
    if not _user_has_role(doctor_id, "doctor"):
        raise ValueError("Selected doctor is not a valid doctor.")

    # Parse timestamp safely
    try:
        appt_ts = _parse_appointment_datetime(appt_date, appt_time)
    except ValueError:
        raise ValueError("Invalid appointment date or time")
    
    # Authorizing rules
    
    # Admin, full access
    if user.has_permission("manage_appointments"):
        created_by_staff = user.id

    # Clinic_receptionist, full CREATE access
    elif user.has_role("clinic_receptionist"):
        created_by_staff = user.id
    
    # Patient, self application creation
    elif user.has_permission("create_appointments") and user.has_role("patient"):
        if patient_id != user.id:
            raise ValueError("Patient can only create appointments for themselves")
        created_by_staff = None
    
    else:
        raise ValueError("User is not allowed to create appointments")
    
    # Insert appointment atomically
    with transaction():
        _, appointment_id = execute(
            """
            INSERT INTO appointments (patient_id, doctor_id, appointment_timestamp, notes, created_by_staff)
            VALUES (%s, %s, %s, %s, %s)    
            """,
            (patient_id, doctor_id, appt_ts, notes, created_by_staff)
        )

    return appointment_id

def _user_has_role(user_id: int, role_name: str) -> bool:
    """
    Helper function that returns True if the given user_id has the specified role.
    """
    return fetchone(
        """
        SELECT 1
        FROM user_roles ur
        JOIN roles r ON r.id = ur.role_id
        WHERE ur.user_id = %s AND r.name = %s
        LIMIT 1
        """,
        (user_id, role_name)
    ) is not None

def _parse_appointment_datetime(date_str: str, time_str: str) -> datetime:
    """
    Helper function that accepts:
    - date: YYYY-MM-DD
    - time: HH:MM (24h) or HH:MM AM/PM (12h)
    """
    datetime_str = f"{date_str} {time_str}".strip()

    formats = [
        "%Y-%m-%d %H:%M",       # 24h
        "%Y-%m-%d %I:%M %p"     # 12h with AM/PM 
    ]

    for format in formats:
        try:
            return datetime.strptime(datetime_str, format)
        except ValueError:
            continue

    raise ValueError("Invalid date or time format")

def update_appointment_status_for(user, data: dict) -> int:
    """
    Update appointment status with strict RBAC and transaction rules.

    Security model:
    - Route must enforce authentication and basic permission checks.
    - Service enforces ownership, role-based authority, and valid state transitions.

    Authorization rules:
    - Admin: 
        - may perform any valid status transition.
    - Clinic receptionist:
        - may confirm, cancel, or mark no_show
        - cancellation requires a reason (notes).
    - Doctor:
        - may only mark appointments as completed
        - only for their own appointments.
    - Patient:
        - may only cancel their own appointments
        - only while status is 'requested'.

    Data integrity:
    - Only valid status transitions are allowed.
    - Status changes are atomic.

    Raises:
        ValueError if authorization or transition is invalid.
    
    Returns:
        appointment_id(int)
    """
    # Extract and validate status update form data
    appointment_id = data.get("appointment_id")
    new_status = data.get("status")
    notes = data.get("notes")

    if not appointment_id or not new_status:
        raise ValueError("Missing required appointment data")
    
    try:
        appointment_id = int(appointment_id)
    except (TypeError, ValueError):
        raise ValueError("Invalid appointment ID")

    # Normalize and validate new_status
    new_status = new_status.lower().strip()

    if new_status not in ALLOWED_STATUSES:
        raise ValueError("Invalid appointment status")
    
    # Fetch and Validate appointment using appointment_id
    appointment = fetchone(
        """
        SELECT id, patient_id, doctor_id, status
        FROM appointments
        WHERE id = %s
        """,
        (appointment_id,)
    )

    if not appointment:
        raise ValueError("Appointment not found")
    
    current_status = appointment["status"]

    # Validate transition
    if current_status not in VALID_TRANSITIONS or new_status not in VALID_TRANSITIONS[current_status]:
        raise ValueError(f"Cannot change status from '{current_status}' to '{new_status}'")
    
    # Authorization rules

    # Admin: any valid transition
    if user.has_permission("manage_appointments"):
        pass

    # Receptionist: confirm, cancel, no_show
    elif user.has_role("clinic_receptionist"):
        if new_status not in {"confirmed", "cancelled", "no_show"}:
            raise ValueError("Receptionist cannot set this status")
        if new_status == "cancelled" and not notes:
            raise ValueError("Cancellation reason is required")
    
    # Doctor: completed (own appointments only)
    elif user.has_role("doctor"):
        if appointment["doctor_id"] != user.id:
            raise ValueError("Doctor can only update their own appointments")
        if new_status != "completed":
            raise ValueError("Doctor can only make appointments as completed")

    # Patient: cancel (own appointments, only if status = requested)
    elif user.has_role("patient"):
        if appointment["patient_id"] != user.id:
            raise ValueError("Patient can only update their own appointments")
        if current_status != "requested" or new_status != "cancelled":
            raise ValueError("Patient can only cancel unconfirmed appointments")
        
    else:
        raise ValueError("User is not allowed to update appointment status")
    
    # Update appointment atomically
    with transaction():
        _, appointment_id = execute(
            """
            UPDATE appointments
            SET status = %s, notes = COALESCE(%s, notes)
            WHERE id = %s
            """,
            (new_status, notes, appointment_id)
        )
    
    return appointment_id

#TODO: In Future Update:
    # Overlapping appointments check (priority:1)
    # Doctor availability check.
    # Appointment in the past.
    # rescheduling
