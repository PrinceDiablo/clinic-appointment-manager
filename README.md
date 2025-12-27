# **Clinic Appointment Manager**

**Clinic Appointment Manager** is a simple web application built with Flask and MySQL. It helps small clinics manage appointments. The goal of this project is to learn how a full-stack Flask app works — from database design to backend scheduling logic to a simple web interface.

---
## **Appointment Lifecycle & Authorization Model**

This application implements a **role and permission-based appointment workflow** designed for a clinic environment.

The core logic lives in the **service layer** and is enforced independently of the UI.

---
## 1. Appointment Lifecycle

Appointments move through a controlled set of states:

- From `requested`
  - requested → confirmed
  - requested → cancelled

- From `confirmed`
  - confirmed → completed
  - confirmed → cancelled
  - confirmed → no_show

Only valid transitions are allowed. Invalid or unauthorized transitions are rejected at the service layer, regardless of UI behavior.

---
## 2. Roles & Permissions Overview

The system uses **RBAC (Role-Based Access Control)** with service-level enforcement. 

Roles are treated as permission bundles. All authorization decisions are ultimately permission-driven and enforced at the service layer.


**Roles**
- **Admin**
- **Clinic Receptionist**
- **Doctor**
- **Patient**

**Key Permissions**
- `create_appointments`
- `view_appointments`
- `manage_appointments`

Permissions are checked at route boundaries, **ownership and scope** are enforced in services.

---
## 3. Who Can Do What?

### Creating Appointments

Rules:

- **Admin / Receptionist**: Can create appointments for any patient

- **Patient**: Can create appointments only for themselves

- **Others**: Not allowed

### Viewing Appointments

Rules:

- **Admin / Receptionist**: All appointments

- **Doctor**: Only their own appointments (with patient name)

- **Patient**: Only their own appointments (with doctor name)

### Updating Appointment Status

Status updates follow strict rules:

**Admin**

- Can perform any valid status transition

**Clinic Receptionist**

- Can: confirmed, cancelled, no_show
- Cancellation requires a reason

**Doctor**

- Can mark appointments as completed
- Only for their own appointments 

**Patient**

- Can cancel only their own 
- Only while status is requested 

All transitions are validated against an explicit state machine.

---
## 4. Security Model

- Routes perform coarse permission checks; services remain the final authority.

- Services enforce:

    - role authority
    - ownership
    - state transitions

- Database writes are atomic using transactions

This design ensures that:

- UI bugs cannot bypass authorization
- Business rules are enforced consistently

---
## 5. Design Notes

- Appointment deletion is intentionally not implemented

- Soft-delete `(deleted_at)` is reserved for future use

- UI may expose filtering and status changes, but never controls authorization

- Permissions are intentionally not editable at runtime and are defined in code to prevent accidental or unauthorized privilege escalation.

---
## 6. Why This Design?

This structure prioritizes:

- service-level security
- long-term extensibility without refactoring core logic

It reflects how production systems protect workflow integrity by enforcing authorization at the service layer rather than relying on UI constraints.

---