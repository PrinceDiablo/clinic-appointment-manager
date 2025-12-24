from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import bp
from app.db import fetchone, execute_commit
from app.auth.models import User
from app.utils.navigation import landing_for_user

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("auth/login.html")

    # User reached route via POST
    # Collect form data
    user_name = request.form.get("user_name", "").strip()
    password = request.form.get("password")

    # Ensure username and password was submitted
    if not user_name or not password:
        flash("Must provide username and password")
        return render_template("auth/login.html")
    
    # Check valid username and password
    row = fetchone(
        "SELECT id, password_hash FROM users WHERE user_name=%s AND is_active=1", 
        (user_name,)
    )

    if not row or not check_password_hash(row["password_hash"], password):
        flash("Incorrect username or password")
        return render_template("auth/login.html")
    
    # Create user session
    user = User.from_row(row)
    login_user(user)

    # Redirect user to landing page
    flash("Logged in successfully!")
    return redirect(url_for("auth.post_login"))

@bp.route("/post_login", methods=["GET"])
@login_required
def post_login():
    """
    Internal transition endpoint.
    Used only immediately after login.
    NOT to link this route directly.
    """
    endpoint = landing_for_user(current_user)
    return redirect(url_for(endpoint))

    
@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log user out"""

    logout_user()
    flash("Logged out")
    return redirect(url_for("main.index"))

# NOTE: Registration is not yet fully transactional.
# Proper transaction support will be added after
# DB helpers support non-autocommit execution.
@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via GET
    if request.method == "GET":
        return render_template("auth/register.html")
    
    # User reached route via POST
    # Collect form data
    user_name = request.form.get("user_name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")
    
    # Ensure username was submitted
    if not user_name:
        flash("Must provide username")
        return render_template("auth/register.html")
    
    # Ensure email was submitted
    if not email:
        flash("Must provide email")
        return render_template("auth/register.html")

    # Ensure password and confirm password was submitted
    if not password or not confirmation:
        flash("Must provide password and confirmation")
        return render_template("auth/register.html")

    # Ensure password and confirmation matches
    if password != confirmation:
        flash("Passwords do not match")
        return render_template("auth/register.html")

    # Check dublicates
    if fetchone("SELECT id FROM users WHERE user_name=%s", (user_name,)):
        flash("Username already in use. Please select a different username.")
        return render_template("auth/register.html")
    
    if fetchone("SELECT id FROM users WHERE email=%s", (email,)):
        flash("E-mail already registered")
        return render_template("auth/register.html")

    # Add user and role in the database 
    hashed_password = generate_password_hash(password)

    try:
        _, user_id = execute_commit(
            "INSERT INTO users (user_name, email, password_hash) " \
            "VALUES (%s, %s, %s)", 
            (user_name, email, hashed_password)
        )
        execute_commit(
            "INSERT INTO user_roles (user_id, role_id) " \
            "VALUES (%s, %s)",
            (user_id, 3)
        )
    except Exception:
        flash("Registration failed. Please try again.")
        return render_template("auth/register.html")

    # Redirect user to login page
    flash("Account created successfully. Please log in.")
    return redirect(url_for("auth.login"))
        