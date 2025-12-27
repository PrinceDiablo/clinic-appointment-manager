# **Clinic Appointment Manager**

**Clinic Appointment Manager** is a simple web application built with Flask and MySQL. It helps small clinics manage appointments.

The goal of this project is to understand how a full-stack Flask application is structured — from database design and service-layer business logic to a minimal web interface — with a strong emphasis on correctness and authorization.

---

## **Appointment Lifecycle & Authorization Model**

This application implements a **role- and permission-based workflow** designed for a clinic environment.

All business rules are enforced in the **service layer**, independently of the UI.  
Routes perform coarse permission checks, but services remain the final authority.

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

Roles are treated as **permission bundles**. All authorization decisions are permission-driven, while **ownership and scope** are enforced in services.


**Roles**
- **Admin**
- **Clinic Receptionist**
- **Doctor**
- **Patient**

**Key Permissions**
- `create_appointments`
- `view_appointments`
- `manage_appointments`
- `create_user`

Permissions are checked at route boundaries, business rules are enforced in the service layer.

---
## 3. Who Can Do What?

### Creating Appointments

Rules:

- **Admin / Receptionist** 
  - Can create appointments for any patient

- **Patient** 
  - Can create appointments only for themselves

- **Others**
  - Not allowed

---
### Viewing Appointments

Rules:

- **Admin / Receptionist**
  - All appointments

- **Doctor** 
  - Only their own appointments (with patient name)

- **Patient** 
  - Only their own appointments (with doctor name)

---

### Updating Appointment Status

Status updates follow strict rules:

- **Admin**
  - Can perform any valid status transition

- **Clinic Receptionist**
  - Can: confirmed, cancelled, no_show
  - Cancellation requires a reason

- **Doctor**
  - Can mark appointments as completed
  - Only for their own appointments 

- **Patient**
  - Can cancel only their own 
  - Only while status is requested 

All transitions are validated against an explicit state machine.

---
## 4. User Account Creation Model

All appointments must be associated with a **user account**.

In real clinic workflows, patients may not always have an existing account at the time of booking.  
To support this, the system allows **authorized staff** to create patient accounts on behalf of patients.

This model follows these rules:

- Every appointment is tied to a user account
- Patients may exist without self-registration
- Authorized staff may create patient accounts
- This action is controlled by a dedicated permission (`create_user`)
- Users created under permission (`create_user`) are always assigned the `patient` role
- User creation may occur as part of the appointment creation workflow
- The UI does not decide whether a user is created; the service layer enforces this rule

This approach maintains a single, consistent identity model while supporting real-world clinic operations.

---
## 5. Security Model

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
## 6. Design Notes

- Appointment deletion is intentionally not implemented
- Soft-delete `(deleted_at)` is reserved for future use
- UI may expose filtering and status changes, but never controls authorization
- Permissions are intentionally not editable at runtime and are defined in code to prevent accidental or unauthorized privilege escalation.
- Staff-created user accounts currently use a temporary default password. This is a conscious trade-off during early development and will be replaced with a proper onboarding flow.

---
## 7. Why This Design?

This structure prioritizes:

- service-level security
- clear ownership boundaries
- extensibility without refactoring core logic

It reflects how production systems protect workflow integrity by enforcing authorization and business rules at the service layer rather than relying on UI constraints.

---