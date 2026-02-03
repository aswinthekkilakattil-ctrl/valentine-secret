import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# ENV VARS (set in Render)
BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_NAME = os.getenv("SENDER_NAME", "Valentine Surprise")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:5000")

# Brevo config
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key["api-key"] = BREVO_API_KEY

api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
    sib_api_v3_sdk.ApiClient(configuration)
)


def send_day_mail(session, day_number):
    link = f"{BASE_URL}/unlock/{session.id}/{day_number}"
    unsubscribe_link = f"{BASE_URL}/unsubscribe/{session.id}"

    html = f"""
    <p>Hi {session.partner_name},</p>

    <p>You have a Valentine surprise waiting 💖</p>

    <p>
        Answer today’s question to unlock it:<br>
        <a href="{link}">Unlock today’s surprise 💌</a>
    </p>

    <hr>
    <p style="font-size:12px;color:#777;">
        Don’t want these emails anymore?
        <a href="{unsubscribe_link}">Unsubscribe</a>
    </p>
    """

    send_email(
        to_email=session.partner_email,
        subject="💌 Valentine Surprise",
        html=html
    )


def send_finale_mail(session):
    link = f"{BASE_URL}/finale/{session.id}"
    unsubscribe_link = f"{BASE_URL}/unsubscribe/{session.id}"

    html = f"""
    <h2>Hi {session.partner_name} 💖</h2>

    <p>Today is Valentine’s Day.</p>
    <p>No questions. No locks.</p>
    <p>Just one final message 💕</p>

    <p>
        <a href="{link}">Open your Valentine surprise 💖</a>
    </p>

    <hr>
    <p style="font-size:12px;color:#777;">
        <a href="{unsubscribe_link}">Unsubscribe</a>
    </p>
    """

    send_email(
        to_email=session.partner_email,
        subject="💖 Happy Valentine’s Day",
        html=html
    )


def send_email(to_email, subject, html):
    try:
        email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": to_email}],
            sender={"email": SENDER_EMAIL, "name": SENDER_NAME},
            subject=subject,
            html_content=html,
        )

        api_instance.send_transac_email(email)
        print(f"✅ Email sent to {to_email}")

    except ApiException as e:
        print("❌ Brevo error:", e)