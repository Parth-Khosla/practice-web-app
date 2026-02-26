from flask import Flask, render_template, request, redirect, session, url_for, abort
from config import Config
from utils.security import bcrypt
from services.auth_service import register_user, login_user
from services.admin_service import promote_to_admin
from models.message_model import create_message, get_user_messages
from models.user_model import find_user_by_username, create_user
from datetime import timedelta
import os

app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = timedelta(seconds=Config.SESSION_TIMEOUT)

bcrypt.init_app(app)

# -------- First Run Admin Creation --------
def create_initial_admin():
    if not find_user_by_username("admin"):
        from utils.security import hash_password
        create_user({
            "username": "admin",
            "password": hash_password("Admin@123"),
            "email": "admin@example.com",
            "phone": "0000000000",
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
@app.route(f"/admin/{Config.ADMIN_URL_SECRET}", methods=["GET", "POST"])
def admin_panel():
    if "username" not in session:
        abort(403)

    user = find_user_by_username(session["username"])
    if user["role"] != "admin":
        abort(403)

    if request.method == "POST":
        promote_to_admin(user, request.form["username"])

    return render_template("admin.html")
    

if __name__ == "__main__":
    app.run(debug=True)