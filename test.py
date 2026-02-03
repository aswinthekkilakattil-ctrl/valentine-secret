from app import app
from models import ValentineSession, DayContent, db

with app.app_context():
    session = ValentineSession.query.first()

    if not session:
        print("❌ No ValentineSession found")
        exit()

    print("✅ Using Session ID:", session.id)

    # Check if Day 8 already exists
    day8 = DayContent.query.filter_by(
        session_id=session.id,
        day_number=8
    ).first()

    if day8:
        print("⚠️ Day 8 already exists")
        print("Secret message:", repr(day8.secret_message))
    else:
        day8 = DayContent(
            session_id=session.id,
            day_number=8,
            answer_hash="FINAL_DAY",   # REQUIRED placeholder
            secret_message=(
                "All these little efforts were just my way of making you smile.\n\n"
                "I didn’t plan this to impress you.\n"
                "I planned it because you matter to me.\n\n"
                "So here it is, straight from my heart:\n"
                "Will you be my Valentine? ❤️"
            ),
            is_unlocked=True
        )

        db.session.add(day8)
        db.session.commit()
        print("🎉 Day 8 CREATED successfully in INSTANCE database")
