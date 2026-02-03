from datetime import date
from models import (
    ValentineSession,
    DayQuestion,
    SystemSettings
)
from email_utils import send_day_mail, send_finale_mail

# Map calendar date → day number
VALENTINE_DAYS = {
    date(2026, 2, 7): 1,
    date(2026, 2, 8): 2,
    date(2026, 2, 9): 3,
    date(2026, 2, 10): 4,
    date(2026, 2, 11): 5,
    date(2026, 2, 12): 6,
    date(2026, 2, 13): 7,
    date(2026, 2, 14): 8,  # Valentine’s Day
}


# ---------- GLOBAL MAIL CHECK ----------
def mails_allowed():
    settings = SystemSettings.query.first()
    if not settings:
        return True   # ✅ default = mails ON
    return settings.mails_enabled


# ---------- DAILY SCHEDULER ----------
def run_daily_scheduler(app):
    today = date(2026, 2, 8)

    # Not a Valentine week day
    if today not in VALENTINE_DAYS:
        print("ℹ️ Not a Valentine day, scheduler skipped")
        return

    day_number = VALENTINE_DAYS[today]

    with app.app_context():

        # 1️⃣ Global admin mail switch
        if not mails_allowed():
            print("🚫 Global mails disabled by admin")
            return

        sessions = ValentineSession.query.all()

        for session in sessions:

            # 2️⃣ Per-user mail switch (sender / partner / admin)
            if not session.mails_enabled:
                print(f"⏸️ Mails paused for session {session.id}")
                continue

            # 3️⃣ Valentine Day (NO question)
            if day_number == 8:
                print(f"💖 Sending Valentine finale mail to session {session.id}")
                send_finale_mail(session)
                continue

            # 4️⃣ Day 1–7 logic
            day = DayQuestion.query.filter_by(
                session_id=session.id,
                day_number=day_number
            ).first()

            # Send mail only if not yet unlocked
            if day and not day.is_unlocked:
                print(f"📧 Sending Day {day_number} mail to session {session.id}")
                send_day_mail(session, day_number)
