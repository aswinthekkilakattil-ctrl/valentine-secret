import os
import smtplib
from email.mime.text import MIMEText


def send_day_mail(session, day_number):
    link = f"http://127.0.0.1:5000/unlock/{session.id}/{day_number}"
    unsubscribe_link = f"http://127.0.0.1:5000/unsubscribe/{session.id}"

    body = f"""
Hi {session.partner_name},

You have a Valentine surprise waiting 💖

Answer today’s question to unlock it:
{link}

---
Don’t want these emails anymore?
Unsubscribe here:
{unsubscribe_link}
"""

    msg = MIMEText(body)
    msg["Subject"] = "💌 Valentine Surprise"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = session.partner_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(
        os.getenv("EMAIL_ADDRESS"),
        os.getenv("EMAIL_PASSWORD")
    )
    server.send_message(msg)
    server.quit()


def send_finale_mail(session):
    link = f"http://127.0.0.1:5000/finale/{session.id}"
    unsubscribe_link = f"http://127.0.0.1:5000/unsubscribe/{session.id}"

    body = f"""
Hi {session.partner_name},

Today is Valentine’s Day 💖

No questions.
No locks.
Just one final message.

Open it here:
{link}

---
Unsubscribe:
{unsubscribe_link}
"""

    msg = MIMEText(body)
    msg["Subject"] = "💖 Happy Valentine’s Day"
    msg["From"] = os.getenv("EMAIL_ADDRESS")
    msg["To"] = session.partner_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(
        os.getenv("EMAIL_ADDRESS"),
        os.getenv("EMAIL_PASSWORD")
    )
    server.send_message(msg)
    server.quit()
