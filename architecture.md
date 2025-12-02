# Architecture of **Clinic Appointment Manager** (CAM)

## Authentication Layer
- Flask-login
- Werkzeug password hashing
- Roles stored in db `user.role`
- Session cookie automatically maintained by **Flask**
- `@login_required` and `@roles_required` decorators

## API Layer

- RESTful routes
- Blueprints -> `/auth` , `/appointments` , `/patients`, `/staff`

## Frontend

- Jinja Templates + Bootstrap 
- Future: replace with **React**

## Database
- MySQL

## File Structure

    Clinic Appointment Manager(CAM)/
    │── app/
    │     └── __init__.py
    │
    │── db/
    │     └── schema.sql
    │
    │── ui/
    │     ├── templates/
    │     │      └── default.html
    │     └── static/
    │
    └── other files