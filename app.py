from flask import Flask, send_from_directory
from flask_login import LoginManager
from models import db, Account
from globals import CATEGORIES, APP_ROOT, UPLOAD_FOLDER, SECRET_KEY
from flask_bcrypt import Bcrypt
import os
from datetime import datetime

from views import main_view
from login import login_view
from admin import admin_view

app = Flask(__name__)
app.register_blueprint(main_view)
app.register_blueprint(login_view)
app.register_blueprint(admin_view)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{APP_ROOT}/db/RattlersUnite2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = SECRET_KEY
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.jinja_env.globals.update(CATEGORIES=CATEGORIES)

bcrypt = Bcrypt(app)

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id: int):
    user = Account.query.get(user_id)
    if user:
        return user
    return None


## Filter Functions
@app.template_filter()
def format_datetime(start: datetime, end: datetime):
    """
    This function takes a string that is in ISO format and converts it
    to a string in datetime format.
    """

    if start.day == end.day:
        startStr = datetime.strftime(start, "%b %d | %I:%M%p")
        endStr = datetime.strftime(end, " - %I:%M%p CT")
    else:
        startStr = datetime.strftime(start, "%b %d - %I:%M%p")
        endStr = datetime.strftime(end, " to %b %d - %I:%M%p CT")
    return startStr + endStr


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


@app.template_filter()
def text_limiter(text: str, org=False):
    if not org:
        if len(text) > 32:
            return text[:32] + "..."
        return text
    else:
        if len(text) > 34:
            return text[:34] + "..."
        return text


def pre_start():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    for f in ["banners", "icons", "profile_icons"]:
        if not os.path.exists(os.path.join(UPLOAD_FOLDER, f)):
            os.makedirs(os.path.join(UPLOAD_FOLDER, f))


if __name__ == "__main__":
    pre_start()
    app.run()
