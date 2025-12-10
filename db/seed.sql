-- ROLES
INSERT INTO roles (id, name, description) VALUES
(1, 'admin', 'System administrator'),
(2, 'doctor', 'Medical doctor'),
(3, 'patient', 'Registered patient');

-- PERMISSIONS
INSERT INTO permissions (id, name, description) VALUES
(1, 'manage_users', 'Create/update/delete users and roles'),
(2, 'view_all_appointments', 'View all appointments (staff/admin)'),
(3, 'manage_appointments', 'Confirm/cancel appointments (doctors/staff)'),
(4, 'create_appointments', 'Create appointment requests (patients/staff)'),
(5, 'view_own_appointments', 'View only own appointments (patients/doctors)'),
(6, 'manage_doctors', 'Create/update doctor details'),
(7, 'manage_permissions', 'Manage role permissions');

-- ROLE -> PERMISSION MAPPING
INSERT INTO role_permissions (role_id, permission_id) VALUES
-- admin
(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),
-- doctor
(2,2),(2,3),(2,5),
-- patient
(3,4),(3,5);

-- USERS(seed pass same as user_name)
INSERT INTO users (id, user_name, email, password_hash, contact_no, is_active)
VALUES
(1, 'admin', 'admin@example.com', 'admin', '9999999999', 1),
(2, 'dr_john', 'john@example.com', 'dr_john', '9000000001', 1),
(3, 'dr_smith', 'smith@example.com', 'dr_smith', '9000000002', 1),
(4, 'dr_khan', 'khan@example.com', 'dr_khan', '9000000003', 1),
(5, 'pat_rahul', 'rahul@example.com', 'pat_rahul', '8000000001', 1),
(6, 'pat_anjali', 'anjali@example.com', 'pat_anjali', '8000000002', 1),
(7, 'pat_karan', 'karan@example.com', 'pat_karan', '8000000003', 1),
(8, 'pat_sneha', 'sneha@example.com', 'pat_sneha', '8000000004', 1),
(9, 'pat_mohan', 'mohan@example.com', 'pat_mohan', '8000000005', 1),
(10,'dev_user', 'dev@example.com', 'dev_user', '7000000000', 1);

-- USER DETAILS
INSERT INTO user_details (user_id, name, dob, gender, address_line1, city, country)
VALUES
(1, 'System Admin', '1990-01-01', 'M', 'Admin House', 'Delhi', 'India'),
(2, 'Dr. John Abraham', '1980-05-10', 'M', 'Clinic Street 1', 'Delhi', 'India'),
(3, 'Dr. Sarah Smith', '1985-08-20', 'F', 'Clinic Street 2', 'Delhi', 'India'),
(4, 'Dr. Imran Khan', '1978-12-01', 'M', 'Clinic Street 3', 'Delhi', 'India'),
(5, 'Rahul Verma', '2000-01-10', 'M', 'Some Address', 'Delhi', 'India'),
(6, 'Anjali Rao', '1998-02-13', 'F', 'Some Address', 'Mumbai', 'India'),
(7, 'Karan Patel', '1995-07-15', 'M', 'Some Address', 'Surat', 'India'),
(8, 'Sneha Gupta', '1999-11-20', 'F', 'Some Address', 'Pune', 'India'),
(9, 'Mohan Lal', '1988-03-05', 'M', 'Some Address', 'Jaipur', 'India'),
(10,'Dev Tester', '1995-06-06', 'M', 'Dev House', 'Local', 'India');

-- USER ROLES
INSERT INTO user_roles (user_id, role_id) VALUES
(1, 1), -- admin
(2, 2), -- doctors
(3, 2),
(4, 2),
(5, 3), -- patients
(6, 3),
(7, 3),
(8, 3),
(9, 3),
(10, 1); -- dev_user as admin for Flask-login testing

-- DOCTOR DETAILS (matches your corrected table)
INSERT INTO doctor_details (user_id, specialization, licence_no, fees)
VALUES
(2, 'General Medicine', 'LIC-DR-JOHN-001', 500),
(3, 'Pediatrics', 'LIC-DR-SMITH-002', 600),
(4, 'Cardiology', 'LIC-DR-KHAN-003', 800);

-- DOCTOR AVAILABILITY
INSERT INTO doctor_availability (user_id, day, start_time, slot_duration_minutes)
VALUES
(2, 'MON', '10:00:00', 30),
(2, 'WED', '10:00:00', 30),
(3, 'TUE', '11:00:00', 30),
(3, 'THU', '11:00:00', 30),
(4, 'FRI', '09:00:00', 30),
(4, 'SAT', '09:00:00', 30);