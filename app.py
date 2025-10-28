from flask import Flask, jsonify, request, session
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allow frontend from Vercel to connect

# Security key (change this before deploying)
app.secret_key = "replace_this_with_a_secure_secret_key"

# Session lifetime: 72 hours (3 days)
app.permanent_session_lifetime = timedelta(hours=72)

# ---------------------------
# Decorator to check session expiry
# ---------------------------
def session_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        expiry = session.get("expiry")
        user = session.get("user")
        if not expiry or datetime.utcnow() > expiry:
            session.clear()
            return jsonify({"error": "Session expired. Please log in again."}), 401
        if not user:
            return jsonify({"error": "Unauthorized access."}), 401
        return f(*args, **kwargs)
    return decorated

# ---------------------------
# Routes
# ---------------------------

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Instascope backend!"})

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # This is a placeholder – later you’ll connect to a real DB
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    # Simulate signup success and start 3-day free trial
    session["user"] = username
    session["expiry"] = datetime.utcnow() + timedelta(hours=72)
    session.permanent = True

    return jsonify({
        "message": "Signup successful. You have a 3-day free trial.",
        "trial_expires": str(session["expiry"])
    }), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Temporary check (replace with real DB validation later)
    if not username or not password:
        return jsonify({"error": "Invalid credentials"}), 400

    session["user"] = username
    session["expiry"] = datetime.utcnow() + timedelta(hours=72)
    session.permanent = True

    return jsonify({
        "message": "Login successful.",
        "expires_in": "72 hours",
        "expiry": str(session["expiry"])
    })


@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/dashboard", methods=["GET"])
@session_required
def dashboard():
    user = session["user"]
    expiry = session["expiry"]
    return jsonify({
        "message": f"Welcome back, {user}!",
        "session_valid_until": str(expiry)
    })


# ---------------------------
# Main entry point
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)
