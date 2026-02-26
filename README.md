# Try2 Web Application

This repository contains a small Flask‑based web application demonstrating
user authentication, role‑based access control, session management, and a
minimal admin panel backed by MongoDB.  It is designed for learning and
lightweight internal use; security best practices are followed where
appropriate but the code is not production hardened.

---

## 📦 Technologies & Libraries Used

- **Python 3.11+** – the language used for the application.
- **Flask** – microframework providing routing, templating, and session
  management.
- **PyMongo** – MongoDB driver for Python; users and messages are stored
  in a MongoDB collection.
- **python-dotenv** – loads configuration from a `.env` file.
- **Flask-Bcrypt** – password hashing and verification.
- **Jinja2** (via Flask) – HTML templating for views.

External requirements (in `requirements.txt`):

```
Flask
pymongo
python-dotenv
flask-bcrypt
```

---

## ⚙️ Configuration

All runtime configuration is loaded from environment variables
(`dotenv` will read `.env` in the project root).  The following keys must
be set:

| Variable              | Description | Example/default |
|-----------------------|-------------|-----------------|
| `SECRET_KEY`          | Flask secret key for signing sessions | `some-secret` |
| `MONGO_URI`           | MongoDB connection URI | `mongodb://...` |
| `DB_NAME`             | Name of the database to use | `mydb` |
| `ADMIN_URL_SECRET`    | Secret slug appended to `/admin/` | `admin` |
| `SESSION_TIMEOUT`     | Inactivity timeout in seconds | `120` |
| `ADMIN_USERNAME`      | Initial admin username (first run)
| `ADMIN_PASSWORD`      | Initial admin password (hashed internally)
| `ADMIN_EMAIL`         | Initial admin email
| `ADMIN_PHONE`         | Initial admin phone number

A sample `.env` with comments is included; copy or modify it to suit your
installation.

### Admin Account Creation

On the very first start of the application, if no user exists with the
username specified by `ADMIN_USERNAME`, an administrator account is
created automatically using the supplied credentials.  This only occurs
once; subsequent runs will not overwrite or recreate the account.

---

## 🚀 Running the Application

1. **Install dependencies** (inside a virtual environment):

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

2. **Populate `.env`** with the required variables (see previous section).

3. **Start the server**:

    ```bash
    python app.py
    ```

4. Visit `http://localhost:5000` in your browser.  You will be redirected
to `/login`.

---

## 🧩 Application Features

### 🔐 Authentication

- **Registration** (`/register`): users may sign up with username,
  password, email, and phone number. Passwords are hashed with bcrypt.
- **Login** (`/login`): valid credentials create a permanent session.
- **Logout** (`/logout`): clears the session.
- **Session timeout**: if a user is inactive for more than
  `SESSION_TIMEOUT` seconds, the session is invalidated and they are
  redirected to the login page.  Activity timestamps are stored in the
  session as ISO strings to avoid timezone mismatches.

### 📝 Dashboard

- Authenticated users are taken to `/dashboard` where
  they can post simple messages (title + body).
- Messages are stored in MongoDB and scoped to the posting user.
- The dashboard displays all messages authored by the logged‑in user.

### 🛠️ Admin Panel

Accessible only to users with `role == 'admin'` at `/admin/<secret>`.

- **Promote user**: enter a username and submit to grant admin rights.
- **Remove user**: delete any user except yourself.  This permanently
  removes the user document from the database.
- **User list**: the panel displays all users (password hashes omitted)
  along with their roles.

Routes and service functions enforce that only administrators can perform
these actions; attempts by non-admins return HTTP 403.

---

## 🔒 Security Considerations

- **Passwords** are hashed with bcrypt using `Flask-Bcrypt` before storage.
- **Sessions** are stored server‑side (Flask's default cookie-based
  sessions) and signed with `SECRET_KEY`.  `SESSION_REFRESH_EACH_REQUEST`
  is disabled to prevent sliding expiration; inactivity is enforced
  manually.
- **Admin URL obfuscation**: the admin panel is mounted at
  `/admin/<ADMIN_URL_SECRET>` to avoid an easily guessable endpoint.
  This is **not** a security barrier; proper role checking is still
  performed on every request.
- **Environment variables** are used for secrets (no hard‑coded
  credentials in source code).
- **Input validation** is minimal; user-supplied values are inserted
  directly into MongoDB queries.  In a production system you would
  sanitize inputs and configure proper indexing to avoid injection.
- **Deletion**: admin user removal does not cascade to messages; those
  remain orphaned.  A production app would either cascade delete
  or disable accounts instead of hard deleting.
- No CSRF protection is implemented (Flask-WTF can be added for this).
- The application runs with `debug=True` in `app.py`.  Disable debug and
  use a proper WSGI server in production.

---

## 📁 Project Structure

```
app.py                # main Flask application
config.py             # configuration class
models/               # database access functions
 services/            # business logic for auth/admin
 templates/           # HTML templates
 utils/                # helper utilities (password hashing, etc.)
 .env                 # environment variables (not committed normally)
 requirements.txt     # Python dependencies
 README.md            # this document
```

---

## 🧪 Testing & Development

There are no automated tests bundled.  For manual testing, run the
application and exercise the following flows:

1. Register a new user and log in.
2. Post messages on the dashboard.
3. Wait past the timeout and try refreshing to confirm logout.
4. Log in as admin (initial credentials from `.env`) and:
   - Promote a normal user and re-login to see the admin panel.
   - Remove a user and confirm they can no longer log in.
   - Verify the user list shows accurate roles.

---

## 📝 Notes

This project is intentionally simple and meant as a learning
exercise.  🛎️ If you plan to deploy it publicly, ensure you add proper
input validation, CSRF protection, HTTPS, rate limiting, error handling,
and audit logging.

Feel free to fork, extend, or use pieces as a starting point for your
own applications!
