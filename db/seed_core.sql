-- ROLES
INSERT INTO roles (id, name, description) VALUES
(1, 'admin', 'System administrator'),
(2, 'doctor', 'Medical doctor'),
(3, 'patient', 'Registered patient'),
(4, 'staff', 'Registered Staff'),
(5, 'clinic_receptionist', 'Manages Appointments')

-- PERMISSIONS
INSERT INTO permissions (id, name, description) VALUES
(1, 'manage_permissions', 'Manage role permissions'),
(2, 'manage_users', 'Manage users and roles'),
(3, 'manage_appointments', 'Manage appointments'),
(4, 'manage_doctors', 'Manage doctor details'),
(5, 'create_appointments', 'Create appointment (patients/staff(cr))'),
(6, 'view_appointments', 'View appointments (staff(cr), limited scope:patients/doctors)'),
(7, 'update_appointments', 'Update appointment status (limited scope:staff(cr)/patients/doctors'),
(8, 'create_user', 'Create users on request and recorded(limited scope:staff)'),
(9, 'view_user', 'users own detailed view(in profile)'),
(10, 'update_user', 'Update users own details(in profile)'),
(11, 'view_doctors', 'doctors own view with availability(in profile)')
(12, 'update_doctors', 'Update doctors own details and limited availability(in profile)'),

-- ROLE -> PERMISSION MAPPING
INSERT INTO role_permissions (role_id, permission_id) VALUES
-- admin
(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(1,11),(1,12)
-- doctor
(2,6),(2,7),(2,9),(2,10),(2,11),(2,12)
-- patient
(3,5),(3,6),(3,7),(3,9),(3,10)
-- staff, clinic_receptionist
(5,5),(5,6),(5,7),(5,8),(5,9),(5,10)
