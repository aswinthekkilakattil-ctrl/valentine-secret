import os
import requests

def send_day_mail(session, day_number):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": os.getenv("BREVO_SENDER_NAME"),
            "email": os.getenv("BREVO_SENDER_EMAIL")
        },
        "to": [
            {"email": session.partner_email, "name": session.partner_name}
        ],
        "subject": "💌 Valentine Surprise",
        "htmlContent": f"""
        <p>Hi {session.partner_name},</p>
        <p>You have a Valentine surprise waiting 💖</p>
        <p>
          <a href="{os.getenv('BASE_URL')}/unlock/{session.id}/{day_number}">
          Unlock today’s surprise
          </a>
        </p>
        <hr>
        <p>
          <a href="{os.getenv('BASE_URL')}/unsubscribe/{session.id}">
          Unsubscribe
          </a>
        </p>
        """
    }

    headers = {
        "accept": "application/json",
        "api-key": os.getenv("BREVO_API_KEY"),
        "content-type": "application/json"
    }

    r = requests.post(url, json=payload, headers=headers)
    print("📨 Brevo response:", r.status_code, r.text)