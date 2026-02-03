import os
import smtplib
import socket
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_TIMEOUT = 10  # seconds


def _send_email(to_email, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = to_email

    try:
        server = smtplib.SMTP_SSL(
            SMTP_HOST,
            SMTP_PORT,
            timeout=SMTP_TIMEOUT
        )
        server.login(
            os.getenv("EMAIL_ADDRESS"),
            os.getenv("EMAIL_PASSWORD")
        )
        server.send_message(msg)
        server.quit()
        print(f"✅ Mail sent to {to_email}")
    except (smtplib.SMTPException, socket.timeout) as e:
        print("❌ SMTP error:", e)
        return False

    return True


def send_day_mail(session, day_number):
    base_url = os.getenv("BASE_URL", "http://localhost:5000")

    body = f"""
Hi {session.partner_name},

You have a Valentine surprise waiting 💖

Answer today’s question to unlock it:
{base_url}/unlock/{session.id}/{day_number}

---
Don’t want these emails anymore?
Unsubscribe here:
{base_url}/unsubscribe/{session.id}
"""

    return _send_email(
        session.partner_email,
        "💌 Valentine Surprise",
        body
    )


def send_finale_mail(session):
    base_url = os.getenv("BASE_URL", "http://localhost:5000")

    body = f"""
Hi {session.partner_name},

Today is Valentine’s Day 💖

No questions.
No locks.
Just one final message.

Open it here:
{base_url}/finale/{session.id}

---
Unsubscribe:
{base_url}/unsubscribe/{session.id}
"""

    return _send_email(
        session.partner_email,
        "💖 Happy Valentine’s Day",
        body
    )