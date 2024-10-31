from flask import Flask, render_template, Blueprint, request
import smtplib
from smtplib import SMTPException
import os
from dotenv import load_dotenv

load_dotenv()

# Configure smtp settings
smtp_server = "smtp.gmail.com"
smtp_port = 587
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

contact_bp = Blueprint("contact", __name__)

@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    msg_sent = False
    if request.method == "POST":
        data = request.form
        if send_email(data["name"], data["email"], data["phone"], data["message"]):
            msg_sent = True
        return render_template("contact.html", msg_sent=msg_sent)
    return render_template("contact.html", msg_sent=msg_sent)


def send_email(name, email, phone, message):
    try:
        email_message = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        with smtplib.SMTP(smtp_server, smtp_port) as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(EMAIL, EMAIL, email_message)
        return True
    except SMTPException as e:
        print(f"SMTP Error: {e}")
        return False
