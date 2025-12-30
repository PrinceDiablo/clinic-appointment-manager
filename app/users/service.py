"""
User domain service.

This module contains user-related business logic, including:
- Controlled creation of user accounts by authorized staff
- Enforcement of role assignment rules for removal rules
- Administrative listing of users and their roles

Security model:
- Callers must be authenticated
- Permission checks are enforced at the service layer
- This module does not expose routes or UI concerns
"""

from werkzeug.security import generate_password_hash
from app.db import fetchone, fetchall, execute, transaction

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
    
def list_users_for(user):
    """
    Return all active users with their roles

    Authorization:
    - manage_users: full view
    - others: empty list

    Behaviour:
    - Returns all active users
    - Returns full role list for admin UI role assignment
    """
     
    if user.has_permission("manage_users"):
        users = fetchall(
            """
            SELECT u.id AS user_id, u.user_name, u.email, u.contact_no, 
                u.last_login, u.failed_logins, u.locked_until, 
                u.created_by_staff, u.created_at, u.updated_at,
                GROUP_CONCAT(DISTINCT r.name ORDER BY r.name) AS roles
            FROM users u
            JOIN user_roles ur ON ur.user_id = u.id
            JOIN roles r ON r.id = ur.role_id
            WHERE is_active = 1
            GROUP BY u.id
            ORDER BY u.user_name
            """
        )

        roles = fetchall("SELECT name FROM roles ORDER BY name")

        return {"users": users, "roles": roles}

    return {"users": [], "roles": []}
    
def assign_role_to(user, data: dict) -> int:
    """
    Assign role to a user

    Authorization:
    - Caller must have the `manage_users` permission.

    Returns:
        Target_user_id(int)
    """
    # Authorization
    if not user.has_permission("manage_users"):
         raise ValueError("User is not allowed to change roles")
    
    # Extract and validate
    target_user_id = data.get("user_id")
    role_name = data.get("role")

    if not target_user_id or not role_name:
         raise ValueError("Missing role assignment data") 
    
    if not fetchone("SELECT id FROM users WHERE id = %s", (target_user_id,)):
        raise ValueError("Target user not found")
   
    row = fetchone("SELECT id FROM roles WHERE name = %s",(role_name,))
    if not row:
        raise ValueError("Role not found") 
    
    role_id = row["id"]

    # Prevent duplicates
    user_role_exists = fetchone(
        """
        SELECT 1 
        FROM user_roles 
        WHERE user_id = %s AND role_id = %s
        LIMIT 1
        """,
        (target_user_id, role_id)
    )
    if user_role_exists:
         raise ValueError("User already has this role")

    # Insert role atomically
    with transaction():
        execute(
            """
            INSERT INTO user_roles (user_id, role_id)
            VALUES (%s, %s)
            """,
            (target_user_id, role_id)
        )
    
    return target_user_id

def remove_role_of(user, data: dict) -> int:
    """
    Remove a role from a user.

    Authorization:
    - Caller must have the `manage_users` permission.

    Behavior:
    - - Can't remove a role the user dosen't have
    - Can't remove the last remaining role
    - Can't remove own `admin` role

    Returns:
        target_user_id (int)
    """

    # Authorization
    if not user.has_permission("manage_users"):
        raise ValueError("User is not allowed to change roles")
    
    # Extract and validate
    target_user_id = data.get("user_id")
    role_name = data.get("role")

    if not target_user_id or not role_name:
        raise ValueError("Missing role removal data")
    
    if not fetchone("SELECT id FROM users WHERE id = %s", (target_user_id,)):
        raise ValueError("Target user not found")
   
    row = fetchone("SELECT id FROM roles WHERE name = %s",(role_name,))
    if not row:
        raise ValueError("Role not found")

    # Prevent self-admin lockout
    if user.id == int(target_user_id) and role_name == "admin":
        raise ValueError("Admin cannot remove their own admin role")

    role_id = row["id"]

    # Ensure user actually have the role
    user_role = fetchone(
        """
        SELECT 1
        FROM user_roles
        WHERE user_id = %s AND role_id = %s
        LIMIT 1
        """,
        (target_user_id, role_id)
    )
    if not user_role:
        raise ValueError("User does not have this role")

    # Count roles (prevent orphan users)
    role_count = fetchone(
        """
        SELECT COUNT(*) AS count
        FROM user_roles
        WHERE user_id = %s
        """,
        (target_user_id,)
    )["count"]

    if role_count <= 1:
        raise ValueError("User must have at least one role")

    # Remove role atomically
    with transaction():
        execute(
            """
            DELETE FROM user_roles
            WHERE user_id = %s AND role_id = %s
            """,
            (target_user_id, role_id)
        )

    return target_user_id