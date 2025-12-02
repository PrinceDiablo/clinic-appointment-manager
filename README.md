# **Clinic Appointment Manager**

**Clinic Appointment Manager** is a simple web application built with Flask and MySQL. It helps small clinics manage appointments, check staff availability, avoid booking conflicts, and send basic email reminders. The goal of this project is to learn how a full-stack Flask app works — from database design to backend scheduling logic to a simple web interface.

---

# ✅ Clinic Appointment Manager — Checklist

## 🔐 Authentication & Roles
- [ ] User login & logout (Flask Login)
- [ ] Role-based access (admin, staff, patient)
- [ ] Password hashing
- [ ] Session management

## 👤 User Management
### Admin
- [ ] Create staff accounts
- [ ] View all users
- [ ] Delete users
- [ ] Reset staff passwords (optional)

### Patient
- [ ] Patient registration
- [ ] Edit personal profile
- [ ] View their appointments

## 🧑‍⚕️ Staff Profiles
- [ ] Staff profile page (name, specialization, contact)
- [ ] Staff availability configuration (working hours, breaks)
- [ ] Staff view their upcoming appointments

## 🗂 Database & Models (MySQL)
- [ ] Users table
- [ ] Staff profile table
- [ ] Patients table
- [ ] Resources table (rooms)
- [ ] Appointments table
- [ ] Notifications table
- [ ] Proper foreign keys + cascading rules

## 🕒 Scheduling & Availability Logic
- [ ] No-overlap appointment logic
- [ ] Time-slot generation (15/30 min intervals)
- [ ] Validate slot availability at booking time
- [ ] Blocked dates / holidays (optional)

## 📅 Appointment Booking
### Patient Side
- [ ] Choose staff → pick date
- [ ] Fetch available time slots
- [ ] Book appointment
- [ ] Cancel appointment (optional)

### Staff/Admin Side
- [ ] View all appointments
- [ ] Update appointment status (optional)
- [ ] Reassign or reschedule appointments (future)

## 🏥 Resource Management (Room Allocation)
- [ ] Attach room to appointment
- [ ] Prevent double-booking of rooms
- [ ] Admin view all room usage

## ✉️ Notifications
- [ ] Email confirmation on booking (Gmail SMTP)
- [ ] Email to staff on new appointment (optional)
- [ ] Appointment reminder email (future)
- [ ] Failed email logging (optional)

## 📊 Admin Dashboard
- [ ] Total staff/patients count
- [ ] Upcoming appointments
- [ ] Most booked staff (optional)
- [ ] Daily/weekly stats (future)

## 🌐 Frontend (Minimal)
- [ ] Basic Bootstrap layout
- [ ] Simple navbar with role-based links
- [ ] Appointment calendar UI (simple list, not JS-heavy)
- [ ] Form validation messages

## 🔒 Security
- [ ] Input validation
- [ ] Prevent SQL injection with parameterized queries
- [ ] Protect admin routes with decorators
- [ ] Env-based config (no plain passwords)
- [ ] CSRF protection (Flask-WTF)

## 🚀 Deployment (Optional for Learning)
- [ ] Docker Compose (Flask + MySQL)
- [ ] Environment variables in `.env`
- [ ] Production config (debug off)
- [ ] Test booking flow in Docker

## 🧪 Tests (Future / Learning)
- [ ] Unit tests for availability logic
- [ ] Test appointment creation & overlap prevention
- [ ] Test API endpoints (optional)

