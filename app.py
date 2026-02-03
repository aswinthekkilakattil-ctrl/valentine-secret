from flask import (
    Flask, render_template, redirect, request, url_for
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, login_required,
    login_user, logout_user, current_user
)
from dotenv import load_dotenv
import hashlib
from datetime import datetime
from flask import session as flask_session

from models import (
    db, User, ValentineSession,
    DayQuestion, ValentineSecret, SystemSettings
)
from questions import QUESTIONS
from story_engine import load_story
from scheduler import run_daily_scheduler

# ---------------- CONFIG ----------------
load_dotenv()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "valentine123"  # change later

# ---------------- APP ----------------
app = Flask(__name__)
app.secret_key = "valentine-secret-key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///valentine.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# ---------------- LOGIN ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------------- HOME ----------------
@app.route("/")
def home():
    return redirect("/login")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            return "User already exists"

        user = User(email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect("/dashboard")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(
            email=request.form["email"]
        ).first()

        if user and user.check_password(
            request.form["password"]
        ):
            login_user(user)
            return redirect("/dashboard")

        return "Invalid email or password"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    session = ValentineSession.query.filter_by(
        user_id=current_user.id
    ).first()

    if not session:
        return redirect("/setup")

    days = DayQuestion.query.filter_by(
        session_id=session.id
    ).order_by(DayQuestion.day_number).all()

    return render_template(
        "dashboard.html",
        session=session,
        days=days
    )


# ---------------- SETUP ----------------
@app.route("/setup", methods=["GET", "POST"])
@login_required
def setup():
    # 🔒 one session per user
    existing = ValentineSession.query.filter_by(
        user_id=current_user.id
    ).first()

    if existing:
        return redirect("/dashboard")

    if request.method == "POST":
        session = ValentineSession(
            user_id=current_user.id,
            sender_name=request.form["sender_name"],
            sender_email=current_user.email,
            partner_name=request.form["partner_name"],
            partner_email=request.form["partner_email"],
        )
        db.session.add(session)
        db.session.commit()

       

           # Day 1–7 questions with MCQ options
        for day in range(1, 8):
            correct = int(request.form[f"day{day}_correct"])

            dq = DayQuestion(
            session_id=session.id,
            day_number=day,
              question=QUESTIONS[day],
              option_1=request.form[f"day{day}_option1"],
              option_2=request.form[f"day{day}_option2"],
              option_3=request.form[f"day{day}_option3"],
              option_4=request.form[f"day{day}_option4"],
              option_5=request.form[f"day{day}_option5"],
              correct_option=correct
              )
            db.session.add(dq)

        # ❤️ Valentine Day secret (Day 8)
        vs = ValentineSecret(
            session_id=session.id,
            secret_message=request.form["valentine_secret"].strip()
        )
        db.session.add(vs)

        db.session.commit()
        return redirect("/dashboard")

    return render_template(
        "setup.html",
        questions=QUESTIONS
    )


# ---------------- UNLOCK (DAY 1–7) ----------------
@app.route("/unlock/<int:session_id>/<int:day_number>", methods=["GET", "POST"])
def unlock(session_id, day_number):
    session = ValentineSession.query.get_or_404(session_id)

    day = DayQuestion.query.filter_by(
        session_id=session_id,
        day_number=day_number
    ).first_or_404()

    # Prepare options safely for Jinja
    options = [
        day.option_1,
        day.option_2,
        day.option_3,
        day.option_4,
        day.option_5
    ]

    # Already unlocked
    if day.is_unlocked:
        story = load_story(day_number, session.sender_name, session.partner_name)
        return render_template("reveal.html", story=story)

    error = None

    if request.method == "POST":
        selected = int(request.form["selected_option"])

        if selected == day.correct_option:
            day.is_unlocked = True
            day.unlocked_at = datetime.utcnow()
            db.session.commit()

            story = load_story(day_number, session.sender_name, session.partner_name)
            return render_template("reveal.html", story=story)
        else:
            error = "Oops 💔 Wrong choice. Try again!"

    return render_template(
        "unlock.html",
        question=day.question,
        day_number=day_number,
        options=options,
        error=error
    )

# ---------------- VALENTINE FINALE ----------------
@app.route("/finale/<int:session_id>")
def finale(session_id):
    session = ValentineSession.query.get_or_404(session_id)

    secret = ValentineSecret.query.filter_by(
        session_id=session.id
    ).first_or_404()

    return render_template(
        "finale.html",
        sender=session.sender_name,
        partner=session.partner_name,
        secret=secret.secret_message
    )


# ---------------- RUN SCHEDULER (TEST) ----------------
@app.route("/run-scheduler")
def run_scheduler():
    run_daily_scheduler(app)
    return "Scheduler executed"



# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if not flask_session.get("admin_logged_in"):
        return redirect("/admin-login")

    sessions = ValentineSession.query.all()
    settings = SystemSettings.query.first()

    mails_enabled = (
        settings.mails_enabled
        if settings else True
    )

    data = []
    for s in sessions:
        days = DayQuestion.query.filter_by(
            session_id=s.id
        ).order_by(DayQuestion.day_number).all()

        secret = ValentineSecret.query.filter_by(
            session_id=s.id
        ).first()

        data.append({
            "session": s,
            "days": days,
            "secret": secret.secret_message if secret else None
        })

    return render_template(
        "admin.html",
        data=data,
        mails_enabled=mails_enabled
    )


# ---------------- ADMIN LOGIN ----------------
@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if (
            request.form["username"] == ADMIN_USERNAME
            and request.form["password"] == ADMIN_PASSWORD
        ):
            flask_session["admin_logged_in"] = True
            return redirect("/admin")

        return "Invalid admin credentials"

    return render_template("admin_login.html")


# ---------------- ADMIN LOGOUT ----------------
@app.route("/admin-logout")
def admin_logout():
    flask_session.pop("admin_logged_in", None)
    return redirect("/admin-login")


# ---------------- GLOBAL MAIL TOGGLE ----------------
@app.route("/admin/toggle-mails")
def toggle_mails():
    if not flask_session.get("admin_logged_in"):
        return redirect("/admin-login")

    settings = SystemSettings.query.first()
    if not settings:
        settings = SystemSettings(mails_enabled=False)
        db.session.add(settings)
    else:
        settings.mails_enabled = not settings.mails_enabled

    db.session.commit()
    return redirect("/admin")


# ---------------- USER MAIL TOGGLE (ADMIN) ----------------
@app.route("/admin/toggle-user-mails/<int:session_id>")
def toggle_user_mails(session_id):
    if not flask_session.get("admin_logged_in"):
        return redirect("/admin-login")

    s = ValentineSession.query.get_or_404(session_id)
    s.mails_enabled = not s.mails_enabled
    db.session.commit()

    return redirect("/admin")


# ---------------- PARTNER UNSUBSCRIBE ----------------
@app.route("/unsubscribe/<int:session_id>")
def unsubscribe(session_id):
    s = ValentineSession.query.get_or_404(session_id)
    s.mails_enabled = False
    db.session.commit()

    return """
    <h2>💔 You are unsubscribed</h2>
    <p>You will no longer receive Valentine mails.</p>
    """


# ---------------- SENDER PAUSE ----------------
@app.route("/toggle-sender-mails", methods=["POST"])
@login_required
def toggle_sender_mails():
    s = ValentineSession.query.filter_by(
        user_id=current_user.id
    ).first_or_404()

    s.mails_enabled = not s.mails_enabled
    db.session.commit()

    return redirect("/dashboard")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)