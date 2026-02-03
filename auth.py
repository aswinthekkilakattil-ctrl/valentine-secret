import os
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized
from flask_login import login_user
from models import User, db

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["profile", "email"],
    redirect_to="dashboard"
)

@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    info = resp.json()

    user = User.query.filter_by(email=info["email"]).first()
    if not user:
        user = User(
            email=info["email"],
            name=info["name"]
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
