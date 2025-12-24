-- ROLES
INSERT INTO roles (id, name, description) VALUES
(1, 'admin', 'System administrator'),
(2, 'doctor', 'Medical doctor'),
(3, 'patient', 'Registered patient'),
(4, 'staff', 'Registered Staff'),
(5, 'clinic_receptionist', 'Manages Appointments')

-- PERMISSIONS
INSERT INTO permissions (id, name, description) VALUES
(1, 'manage_users', 'Create/update/delete users and roles(admin, update on request by doctor/patient/staff)'),
(2, 'manage_appointments', 'Confirm/cancel appointments (staff(cr)/admin)'),
(3, 'create_appointments', 'Create appointment requests (patients/staff(cr))'),
(4, 'view_appointments', 'View appointments (admin/staff(cr), limited scope:patients/doctors)'),
(5, 'manage_doctors', 'Create/update doctor details(admin,update on request by doctor)'),
(6, 'manage_permissions', 'Manage role permissions');

-- ROLE -> PERMISSION MAPPING
INSERT INTO role_permissions (role_id, permission_id) VALUES
-- admin
(1,1),(1,2),(1,3),(1,4),(1,5),(1,6),
-- doctor
(2,4),
-- patient
(3,4),
-- staff, clinic_receptionist
(5,2),(5,3),(5,4)
