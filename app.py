from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash

from utils.database import (
    create_tables,
    add_user,
    check_user,
    save_history,
    get_history,
    get_statistics
)

from utils.url_features import extract_features

import joblib
import re
import os

app = Flask(__name__)
app.secret_key = "smart_phishing_secret_key"

# ------------------------------------
# Create Database
# ------------------------------------

create_tables()

# ------------------------------------
# Load ML Models
# ------------------------------------

sms_model = joblib.load("model/sms_model.pkl")
sms_vectorizer = joblib.load("model/sms_vectorizer.pkl")

email_model = joblib.load("model/email_model.pkl")
email_vectorizer = joblib.load("model/email_vectorizer.pkl")

url_model = joblib.load("model/url_model.pkl")

# ------------------------------------
# Login
# ------------------------------------

@app.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = check_user(email)

        if user and check_password_hash(user[3], password):

            session["user"] = user[1]
            session["email"] = user[2]

            return redirect(url_for("dashboard"))

        else:

            return "Invalid Email or Password"

    return render_template("login.html")


# ------------------------------------
# Register
# ------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        if password != confirm:

            return "Passwords do not match!"

        hashed = generate_password_hash(password)

        success = add_user(name, email, hashed)

        if success:

            return redirect(url_for("login"))

        else:

            return "Email already exists!"

    return render_template("register.html")


# ------------------------------------
# Dashboard
# ------------------------------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(url_for("login"))

    sms, email, url, total = get_statistics(session["email"])

    return render_template(
        "dashboard.html",
        user=session["user"],
        sms=sms,
        email=email,
        url=url,
        total=total
    )
# ------------------------------------
# SMS Scanner
# ------------------------------------

@app.route("/sms", methods=["GET", "POST"])
def sms():

    prediction = None

    if request.method == "POST":

        message = request.form["message"]

        vector = sms_vectorizer.transform([message])

        result = sms_model.predict(vector)[0]

        if result == 1:
            prediction = "🚨 Spam SMS"
        else:
            prediction = "✅ Safe SMS"

        save_history(
            session["email"],
            "SMS",
            message,
            prediction
        )

    return render_template(
        "sms.html",
        prediction=prediction
    )


# ------------------------------------
# Email Scanner
# ------------------------------------

@app.route("/email", methods=["GET", "POST"])
def email():

    prediction = None

    if request.method == "POST":

        email_text = request.form["email_text"]

        vector = email_vectorizer.transform([email_text])

        result = email_model.predict(vector)[0]

        if result == 1:
            prediction = "🚨 Phishing Email"
        else:
            prediction = "✅ Legitimate Email"

        save_history(
            session["email"],
            "Email",
            email_text,
            prediction
        )

    return render_template(
        "email.html",
        prediction=prediction
    )
# ------------------------------------
# URL Scanner
# ------------------------------------

@app.route("/url", methods=["GET", "POST"])
def url():

    prediction = None

    if request.method == "POST":

        website = request.form["url"]

        features = extract_features(website)

        result = url_model.predict(features)[0]

        if result == 1:
            prediction = "🚨 Phishing Website"
        else:
            prediction = "✅ Safe Website"

        save_history(
            session["email"],
            "URL",
            website,
            prediction
        )

    return render_template(
        "url.html",
        prediction=prediction
    )


# ------------------------------------
# Scan History
# ------------------------------------

@app.route("/history")
def history():

    if "user" not in session:
        return redirect(url_for("login"))

    history_data = get_history(session["email"])

    return render_template(
        "history.html",
        history=history_data
    )


# ------------------------------------
# Password Strength Checker
# ------------------------------------

@app.route("/password", methods=["GET", "POST"])
def password():

    strength = None
    score = None
    suggestion = None

    if request.method == "POST":

        pwd = request.form["password"]

        points = 0

        if len(pwd) >= 8:
            points += 1

        if re.search(r"[A-Z]", pwd):
            points += 1

        if re.search(r"[a-z]", pwd):
            points += 1

        if re.search(r"\d", pwd):
            points += 1

        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd):
            points += 1

        if points <= 2:
            strength = "🔴 Weak Password"
            score = "Strength : 30%"
            suggestion = "Use uppercase, lowercase, numbers and special characters."

        elif points <= 4:
            strength = "🟡 Medium Password"
            score = "Strength : 70%"
            suggestion = "Add more symbols and increase password length."

        else:
            strength = "🟢 Strong Password"
            score = "Strength : 100%"
            suggestion = "Excellent! Your password is secure."

    return render_template(
        "password.html",
        strength=strength,
        score=score,
        suggestion=suggestion
    )
# ------------------------------------
# Voice Scam Detection (Coming Soon)
# ------------------------------------

@app.route("/voice")
def voice():

    if "user" not in session:
        return redirect(url_for("login"))

    return render_template("voice.html")


# ------------------------------------
# Logout
# ------------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ------------------------------------
# Run Application
# ------------------------------------

if __name__ == "__main__":

    app.run(debug=True)