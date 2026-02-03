from app import app
from models import db, User, ValentineSession, DayContent

with app.app_context():
    print("Deleting all DayContent...")
    DayContent.query.delete()

    print("Deleting all ValentineSessions...")
    ValentineSession.query.delete()

    print("Deleting all Users...")
    User.query.delete()

    db.session.commit()
    print("✅ ALL USERS AND DATA DELETED SUCCESSFULLY")
