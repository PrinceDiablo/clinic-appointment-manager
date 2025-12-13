from flask import flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from . import bp
from app.db import fetchone, execute_commit
from app.auth.models import User

@bp.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # User reached route via POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return render_template("auth/login.html")

        # Ensure password was submitted
        if not password:
            flash("must provide password")
            return render_template("auth/login.html")
        
        # Check valid username and password
        row = fetchone("SELECT * FROM users WHERE user_name=%s", (username,))
        if not row:
            flash("Incorrect username or password")
            return render_template("auth/login.html")
        
        if len(row) != 1 or not check_password_hash(row["password_hash"], password):
            flash("Incorect username or password")
            return render_template("auth/login.html")
        
        # Create user session
        user = User.from_row(row)
        login_user(user)

        # Redirect user to landing page
        flash("Logged in successfully!")
        return redirect(url_for("main.index"))
    
    # User reached route via GET
    else:
        return render_template("auth/login.html")

    
@bp.route("/logout")
@login_required
def logout():
    """Log user out"""

    logout_user()
    flash("Logged out")
    return redirect(url_for("main.index"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST
    if request.method == "POST":

        username = request.form.get("user_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        # Ensure username was submitted
        if not username:
            flash("must provide username")
            return render_template("auth/register.html")

        # Ensure password was submitted
        if not password:
            flash("must provide password")
            return render_template("auth/register.html")

        # Ensure confirm password was submitted
        if not confirmation:
            flash("must provide confirm password")
            return render_template("auth/register.html")

        # Ensure password and confirmation matches
        if password != confirmation:
            flash("password and confirm password is not same")
            return render_template("auth/register.html")

        # Check for dublicate Username
        if fetchone("SELECT id FROM users WHERE username=%s", (username,)):
            flash("Username already in use. Please select a different username.")
            return render_template("auth/register.html")
        
        # Check for dublicate E-mail
        if fetchone("SELECT id FROM users WHERE username=%s", (email,)):
            flash("E-mail already registered")
            return render_template("auth/register.html")

        # Add user to database 
        hashed_password = generate_password_hash(password)
        execute_commit("INSERT INTO users (username, email, password_hash, role) VALUES (%s, %s, %s, %s)", (username, email, hashed_password, "patient"))
        

        # Redirect user to login page
        flash("Account created. Please log in")
        return redirect(url_for("auth.login"))

    # User reached route via GET
    else:
        return render_template("auth/register.html")
