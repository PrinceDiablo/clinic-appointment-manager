from werkzeug.security import generate_password_hash
from app.db import fetchone, execute_commit

def seed_default_admin():
    count = fetchone("SELECT COUNT(*) AS c FROM users")["c"]
    if count > 0:
        return
    # Insert admin user
    _, user_id = execute_commit(
            """
            INSERT INTO users (user_name, email, password_hash, contact_no)
            VALUES (%s, %s, %s, %s)
            """,
            ('admin', 'admin@example.com', generate_password_hash('admin'), '9999999999')
    )

    # Assign admin role
    role_id = fetchone("SELECT id FROM roles WHERE name = %s",("admin",))["id"]
    execute_commit(
        """
        INSERT INTO user_roles (user_id, role_id)
        VALUES (%s, %s)
        """,
        (user_id, role_id)
    )
