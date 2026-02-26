from flask import Flask, render_template, request, redirect, session, url_for, abort
from config import Config
from utils.security import bcrypt
from services.auth_service import register_user, login_user
from services.admin_service import promote_to_admin, remove_user, list_users
from models.message_model import create_message, get_user_messages
from models.user_model import find_user_by_username, create_user
from datetime import timedelta, datetime
import os

app = Flask(__name__)
app.config.from_object(Config)
# explicitly set lifetime on the config as well as the attribute
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=Config.SESSION_TIMEOUT)
app.permanent_session_lifetime = app.config["PERMANENT_SESSION_LIFETIME"]
# disable automatic refresh of the session cookie; we'll handle inactivity manually
app.config["SESSION_REFRESH_EACH_REQUEST"] = Config.SESSION_REFRESH_EACH_REQUEST

bcrypt.init_app(app)

# -------- First Run Admin Creation --------
def create_initial_admin():
    # create a default administrator account if one doesn't already exist
    if not find_user_by_username(Config.ADMIN_USERNAME):
        from utils.security import hash_password
        create_user({
            "username": Config.ADMIN_USERNAME,
            "password": hash_password(Config.ADMIN_PASSWORD),
            "email": Config.ADMIN_EMAIL,
            "phone": Config.ADMIN_PHONE,
            "role": "admin"
        })
        print("Initial admin created.")

create_initial_admin()

# -------- Routes --------

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = {
            "username": request.form["username"],
            "password": request.form["password"],
            "email": request.form["email"],
            "phone": request.form["phone"]
        }
        register_user(data)
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        success, user = login_user(
            request.form["username"],
            request.form["password"]
        )
        if success:
            session.permanent = True
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect("/login")

    if request.method == "POST":
        create_message({
            "username": session["username"],
            "title": request.form["title"],
            "message": request.form["message"]
        })

    messages = get_user_messages(session["username"])
    return render_template("dashboard.html", messages=messages)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

# -------- Dynamic Admin URL --------
@app.before_request
def enforce_session_timeout():
    # if there is no session or user isn't logged in, nothing to do
    if "username" not in session:
        return

    now = datetime.utcnow()
    last = session.get("last_active")
    if last:
        # session data may come back as a string or with tzinfo; normalize to naive
        if isinstance(last, str):
            try:
                last = datetime.fromisoformat(last)
            except ValueError:
                # abort if parsing fails
                last = None
        elif isinstance(last, datetime) and last.tzinfo is not None:
            last = last.replace(tzinfo=None)

        if last:
            elapsed = now - last
            if elapsed.total_seconds() > Config.SESSION_TIMEOUT:
                # expire the session and redirect to login
                session.clear()
                return redirect(url_for("login"))
    # store ISO string so the cookie serialization is predictable
    session["last_active"] = now.isoformat()


@app.route(f"/admin/{Config.ADMIN_URL_SECRET}", methods=["GET", "POST"])
def admin_panel():
    if "username" not in session:
        abort(403)

    user = find_user_by_username(session["username"])
    if user["role"] != "admin":
        abort(403)

    if request.method == "POST":
        # two possible actions: promote or remove
        if "username" in request.form:
            promote_to_admin(user, request.form["username"])
        elif "remove_username" in request.form:
            remove_user(user, request.form["remove_username"])

    users = list_users()
    return render_template("admin.html", users=users)
    

if __name__ == "__main__":
    app.run(debug=True)