from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_bcrypt import generate_password_hash, check_password_hash
db = SQLAlchemy()


class Event(db.Model):
    __tablename__ = "Events"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    Organization = db.Column(db.Integer, db.ForeignKey("Accounts.id"))
    StartDate = db.Column(db.DateTime, nullable=False)
    EndDate = db.Column(db.DateTime, nullable=False)
    Location = db.Column(db.String, nullable=False, default="St. Mary's University")
    Description = db.Column(db.String, nullable=False)
    Category = db.Column(db.String, nullable=False)
    EventIcon = db.Column(db.String, default="../static/defaults/STMUlogo.jpg")
    EventBanner = db.Column(db.String, default="../static/defaults/STMUlogo.png")

    def __repr__(self):
        return "<Event %r>" % self.Name


class Account(db.Model, UserMixin):
    __tablename__ = "Accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    points = db.Column(db.Integer, nullable=False, default=0)
    about = db.Column(db.String, nullable=False, default="I'm new here. Say hi!")
    icon = db.Column(
        db.String, nullable=False, default="../static/defaults/STMUlogo.jpg"
    )
    staff = db.Column(db.Boolean, default=False, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @staticmethod
    def get_by_username(username):
        return Account.query.filter_by(username=username).first()


class StudentAccount(Account):
    def __init__(self, **properties):
        super().__init__(**properties)


class OrganizationAccount(Account):
    def __init__(self, **properties):
        super().__init__(**properties, staff=True)


class AdminAccount(Account):
    def __init__(self, **properties):
        super().__init__(**properties, staff=True, admin=True)


