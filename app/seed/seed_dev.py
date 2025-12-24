from werkzeug.security import generate_password_hash
from app.db import fetchone, execute_commit

def seed_dev():
    count = fetchone("SELECT COUNT(*) AS c FROM users")["c"]
    if count > 1:
        return
    # USERS
    users = [
        ('dr_john', 'john@example.com', 'dr_john', '9000000001'),
        ('dr_smith', 'smith@example.com', 'dr_smith', '9000000002'),
        ('dr_khan', 'khan@example.com', 'dr_khan', '9000000003'),
        ('pat_rahul', 'rahul@example.com', 'pat_rahul', '8000000001'),
        ('pat_anjali', 'anjali@example.com', 'pat_anjali', '8000000002'),
        ('pat_karan', 'karan@example.com', 'pat_karan', '8000000003'),
        ('pat_sneha', 'sneha@example.com', 'pat_sneha', '8000000004'),
        ('pat_mohan', 'mohan@example.com', 'pat_mohan', '8000000005'),
        ('st_cr_ron', 'ron@example.com', 'st_cr_ron', '7000000001')
    ]

    for username, email, password, phone in users:
        execute_commit(
            """
            INSERT INTO users (user_name, email, password_hash, contact_no)
            VALUES (%s, %s, %s, %s)
            """,
            (username, email, generate_password_hash(password), phone)
        )

    #USER DETAILS
    user_details = [
        ('admin', 'System Admin', '1990-01-01', 'M', 'Admin House', 'Delhi', 'India'),
        ('dr_john', 'Dr. John Abraham', '1980-05-10', 'M', 'Clinic Street 1', 'Delhi', 'India'),
        ('dr_smith', 'Dr. Sarah Smith', '1985-08-20', 'F', 'Clinic Street 2', 'Delhi', 'India'),
        ('dr_khan', 'Dr. Imran Khan', '1978-12-01', 'M', 'Clinic Street 3', 'Delhi', 'India'),
        ('pat_rahul', 'Rahul Verma', '2000-01-10', 'M', 'Some Address', 'Delhi', 'India'),
        ('pat_anjali', 'Anjali Rao', '1998-02-13', 'F', 'Some Address', 'Mumbai', 'India'),
        ('pat_karan', 'Karan Patel', '1995-07-15', 'M', 'Some Address', 'Surat', 'India'),
        ('pat_sneha', 'Sneha Gupta', '1999-11-20', 'F', 'Some Address', 'Pune', 'India'),
        ('pat_mohan', 'Mohan Lal', '1988-03-05', 'M', 'Some Address', 'Jaipur', 'India'),
        ('st_cr_ron', 'Ron Don', '1995-06-06', 'M', 'Ron House', 'Delhi', 'India')
    ]

    for user_name, name, dob, gender, address_line1, city, country in user_details:
        execute_commit(
            """
            INSERT INTO user_details (user_id, name, dob, gender, address_line1, city, country)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (get_user_id(user_name), name, dob, gender, address_line1, city, country)
        )

    # USER ROLES
    user_roles = [
        ('dr_john', 'doctor'),
        ('dr_smith', 'doctor'),
        ('dr_khan', 'doctor'),
        ('pat_rahul', 'patient'),
        ('pat_anjali', 'patient'),
        ('pat_karan', 'patient'),
        ('pat_sneha', 'patient'),
        ('pat_mohan', 'patient'),
        ('st_cr_ron', 'staff'),
        ('st_cr_ron', 'clinic_receptionist')    
    ]

    for user_name, role in user_roles:
        role_id = fetchone("SELECT id FROM roles WHERE name = %s",(role,))["id"]
        execute_commit(
            """
            INSERT INTO user_roles (user_id, role_id)
            VALUES (%s, %s)
            """,
            (get_user_id(user_name), role_id)
        )

    # DOCTOR DETAILS
    doctor_details = [
        ('dr_john', 'General Medicine', 'LIC-DR-JOHN-001', 500),
        ('dr_smith', 'Pediatrics', 'LIC-DR-SMITH-002', 600),
        ('dr_khan', 'Cardiology', 'LIC-DR-KHAN-003', 800)
    ]

    for user_name, specialization, licence_no, fees in doctor_details:
        execute_commit(
            """
            INSERT INTO doctor_details (user_id, specialization, licence_no, fees)
            VALUES (%s, %s, %s, %s)
            """,
            (get_user_id(user_name), specialization, licence_no, fees)
        )

    # DOCTOR AVAILABILITY
    doctor_availability = [
        ('dr_john', 'MON', '10:00:00'),
        ('dr_john', 'WED', '10:00:00'),
        ('dr_smith', 'TUE', '11:00:00'),
        ('dr_smith', 'THU', '11:00:00'),
        ('dr_khan', 'FRI', '09:00:00'),
        ('dr_khan', 'SAT', '09:00:00')
    ]

    for user_name, day, start_time in doctor_availability:
        execute_commit(
            """
            INSERT INTO doctor_availability (user_id, day, start_time)
            VALUES (%s, %s, %s)
            """,
            (get_user_id(user_name), day, start_time)
        )

def get_user_id(n):
    """ get user_id from user_name in users table"""
    return fetchone("SELECT id FROM users WHERE user_name = %s",(n,))["id"]
    