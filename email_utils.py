import os
import requests

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BREVO_SENDER_NAME = os.getenv("BREVO_SENDER_NAME")
BASE_URL = os.getenv("BASE_URL")

BREVO_URL = "https://api.brevo.com/v3/smtp/email"


def send_day_mail(session, day_number):
    link = f"{BASE_URL}/unlock/{session.id}/{day_number}"
    unsubscribe_link = f"{BASE_URL}/unsubscribe/{session.id}"

    payload = {
        "sender": {
            "email": BREVO_SENDER_EMAIL,
            "name": BREVO_SENDER_NAME
        },
        "to": [
            {"email": session.partner_email, "name": session.partner_name}
        ],
        "subject": "💌 Valentine Surprise",
        "htmlContent": f"""
        <p>Hi {session.partner_name},</p>
        <p>You have a Valentine surprise waiting 💖</p>
        <p><a href="{link}">Unlock today’s surprise</a></p>
        <hr>
        <p><a href="{unsubscribe_link}">Unsubscribe</a></p>
        """
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    r = requests.post(BREVO_URL, json=payload, headers=headers)

    if r.status_code >= 400:
        print("❌ Brevo error:", r.status_code, r.text)
    else:
        print("✅ Brevo mail sent:", session.partner_email)


def send_finale_mail(session):
    link = f"{BASE_URL}/finale/{session.id}"

    payload = {
        "sender": {
            "email": BREVO_SENDER_EMAIL,
            "name": BREVO_SENDER_NAME
        },
        "to": [
            {"email": session.partner_email, "name": session.partner_name}
        ],
        "subject": "💖 Happy Valentine’s Day",
        "htmlContent": f"""
        <p>Hi {session.partner_name},</p>
        <p>Today is Valentine’s Day 💖</p>
        <p><a href="{link}">Open your final secret</a></p>
        """
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    r = requests.post(BREVO_URL, json=payload, headers=headers)

    if r.status_code >= 400:
        print("❌ Brevo error:", r.status_code, r.text)
    else:
        print("✅ Finale mail sent")