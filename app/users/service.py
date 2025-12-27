"""
User domain service.

This module contains user-related business logic, including:
- Controlled creation of user accounts by authorized staff
- Enforcement of role assignment rules for system-created users
- Atomic initialization of user, role, and profile data

Security model:
- Callers must be authenticated
- Permission checks are enforced at the service layer
- This module does not expose routes or UI concerns
"""

from werkzeug.security import generate_password_hash
from app.db import fetchone, execute, transaction

# TEMPORARY: system-created users use a default password
# MUST be replaced with reset-on-first-login or token flow
DEFAULT_SYSTEM_PASSWORD = "1234"

def create_user_by_staff(user, data: dict) -> int:
    """
    Create a new patient user on behalf of a patient.

    Authorization:
    - Caller must have the `create_user` permission.

    Behavior:
    - User is created with the `patient` role.
    - Account is marked with `created_by_staff`.
    - User details are initialized atomically.

    Returns:
        user_id(int)
    """

    # Authorizing
    if not user.has_permission("create_user"):
        raise ValueError("User is not allowed to create users")

    # Extract required user registration data
    name = data.get("name", "").strip()
    user_name = data.get("user_name", "").strip()
    email = data.get("email", "").strip()
    
    if not name or not user_name or not email:
        raise ValueError("Missing required user data")
    
    hashed_password = generate_password_hash(DEFAULT_SYSTEM_PASSWORD)
    created_by_staff = user.id

    # Fetching patient role
    patient_role_row = fetchone("SELECT id FROM roles WHERE name = %s",("patient",))
    if not patient_role_row:
        raise ValueError("Registration configuration error.")
    
    patient_role_id = patient_role_row["id"]
    
    # Atomic user creation
    try:
        with transaction():
            # Insert user
                _, user_id = execute(
                    """
                    INSERT INTO users (user_name, email, password_hash, created_by_staff)
                    VALUES (%s, %s, %s, %s)
                    """, 
                    (user_name, email, hashed_password, created_by_staff)
                )
                # Assign default role "patient"
                execute(
                    """
                    INSERT INTO user_roles (user_id, role_id)
                    VALUES (%s, %s)
                    """,
                    (user_id, patient_role_id)
                )
                # Insert name in user_details
                execute(
                    """
                    INSERT INTO user_details (user_id, name)
                    VALUES  (%s, %s)
                    """,
                    (user_id, name)
                )

    except Exception:
         raise ValueError("User creation failed")
    
    return user_id
    
