import os
import requests

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
SENDER_NAME = os.getenv("BREVO_SENDER_NAME", "Valentine 💖")
BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def _send_email(to_email, subject, html_content):
    headers = {
        "api-key": BREVO_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    payload = {
        "sender": {
            "email": SENDER_EMAIL,
            "name": SENDER_NAME
        },
        "to": [
            {"email": to_email}
        ],
        "subject": subject,
        "htmlContent": html_content
    }

    response = requests.post(BREVO_URL, json=payload, headers=headers)

    if response.status_code not in (200, 201, 202):
        print("❌ Brevo error:", response.status_code, response.text)
        return False

    print(f"✅ Email sent to {to_email}")
    return True


def send_day_mail(session, day_number):
    link = f"{BASE_URL}/unlock/{session.id}/{day_number}"
    unsubscribe = f"{BASE_URL}/unsubscribe/{session.id}"

    html = f"""
    <p>Hi <b>{session.partner_name}</b>, 💖</p>

    <p>You have a Valentine surprise waiting for you.</p>

    <p>
        👉 <a href="{link}">Answer today’s question to unlock it</a>
    </p>

    <hr>
    <small>
        Don’t want these emails?
        <a href="{unsubscribe}">Unsubscribe</a>
    </small>
    """

    return _send_email(
        session.partner_email,
        "💌 Valentine Surprise",
        html
    )


def send_finale_mail(session):
    link = f"{BASE_URL}/finale/{session.id}"
    unsubscribe = f"{BASE_URL}/unsubscribe/{session.id}"

    html = f"""
    <p>Hi <b>{session.partner_name}</b>, 💖</p>

    <p><b>Today is Valentine’s Day.</b></p>

    <p>No questions. No locks.</p>

    <p>
        👉 <a href="{link}">Open your final secret message</a>
    </p>

    <hr>
    <small>
        <a href="{unsubscribe}">Unsubscribe</a>
    </small>
    """

    return _send_email(
        session.partner_email,
        "💖 Happy Valentine’s Day",
        html
    )