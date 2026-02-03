from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ---------------- USER ----------------
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ---------------- VALENTINE SESSION ----------------
class ValentineSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        unique=True   # ✅ THIS LINE FIXES IT
    )

    sender_name = db.Column(db.String(100), nullable=False)
    sender_email = db.Column(db.String(120), nullable=False)  # 👈 NEW (see problem 2)
    partner_name = db.Column(db.String(100), nullable=False)
    partner_email = db.Column(db.String(120), nullable=False)

    mails_enabled = db.Column(db.Boolean, default=True)

# ---------------- DAY QUESTIONS (DAY 1–7) ----------------
class DayQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("valentine_session.id"),
        nullable=False
    )

    day_number = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(200), nullable=False)

    option_1 = db.Column(db.String(100), nullable=False)
    option_2 = db.Column(db.String(100), nullable=False)
    option_3 = db.Column(db.String(100), nullable=False)
    option_4 = db.Column(db.String(100), nullable=False)
    option_5 = db.Column(db.String(100), nullable=False)

    correct_option = db.Column(db.Integer, nullable=False)  # 1–5

    is_unlocked = db.Column(db.Boolean, default=False)
    unlocked_at = db.Column(db.DateTime)


# ---------------- VALENTINE FINAL SECRET (DAY 8) ----------------
class ValentineSecret(db.Model):
    __tablename__ = "valentine_secret"

    id = db.Column(db.Integer, primary_key=True)

    session_id = db.Column(
        db.Integer,
        db.ForeignKey("valentine_session.id"),
        unique=True,
        nullable=False
    )

    secret_message = db.Column(db.Text, nullable=False)


# ---------------- SYSTEM SETTINGS (GLOBAL MAIL SWITCH) ----------------
class SystemSettings(db.Model):
    __tablename__ = "system_settings"

    id = db.Column(db.Integer, primary_key=True)
    mails_enabled = db.Column(db.Boolean, default=True)
