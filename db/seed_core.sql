-- ROLES
INSERT INTO roles (id, name, description) VALUES
(1, 'admin', 'System administrator'),
(2, 'doctor', 'Medical doctor'),
(3, 'patient', 'Registered patient'),
(4, 'staff', 'Registered Staff'),
(5, 'clinic_receptionist', 'Manages Appointments')

-- PERMISSIONS
INSERT INTO permissions (id, name, description) VALUES
(1, 'manage_users', 'Manage users and roles'),
(2, 'manage_appointments', 'Manage appointments'),
(3, 'manage_doctors', 'Manage doctor details'),
(4, 'create_appointments', 'Create appointment (patients/staff(cr))'),
(5, 'view_appointments', 'View appointments (staff(cr), limited scope:patients/doctors)'),
(6, 'update_appointments', 'Update appointment status (limited scope:staff(cr)/patients/doctors'),
(7, 'create_user', 'Create users on request and recorded(limited scope:staff)'),
(8, 'view_user', 'users own detailed view(in profile)'),
(9, 'update_user', 'Update users own details(in profile)'),
(10, 'view_doctors', 'doctors own view with availability(in profile)')
(11, 'update_doctors', 'Update doctors own details and limited availability(in profile)'),

-- ROLE -> PERMISSION MAPPING
INSERT INTO role_permissions (role_id, permission_id) VALUES
-- admin
(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11)
-- doctor
(2,5),(2,6),(2,8),(2,9),(2,10),(2,11)
-- patient
(3,4),(3,5),(3,6),(3,8),(3,9)
-- staff, clinic_receptionist
(5,4),(5,5),(5,6),(5,7),(5,8),(5,9)
