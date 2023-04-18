from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import ForeignKey

db = SQLAlchemy()


class Organization(db.Model):
    __tablename__ = "Organizations"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    AboutUs = db.Column(db.String, nullable=False)
    OrgIcon = db.Column(db.String, default="../static/defaults/STMUlogo.jpg")

    def __repr__(self):
        return "<Organization %r>" % self.Name


class Event(db.Model):
    __tablename__ = "Events"

    ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Name = db.Column(db.String, nullable=False)
    Organization = db.Column(db.Integer, db.ForeignKey("Organizations.ID"))
    StartDate = db.Column(db.DateTime, nullable=False, default=datetime.now())
    EndDate = db.Column(
        db.DateTime, nullable=False, default=(datetime.now() + timedelta(1))
    )
    Location = db.Column(db.String, nullable=False, default="St. Mary's University")
    Description = db.Column(db.String, nullable=False)
    Category = db.Column(db.String, nullable=False)
    EventIcon = db.Column(db.String, default="../static/defaults/STMUlogo.jpg")
    EventBanner = db.Column(db.String, default="../static/defaults/STMUlogo.png")

    def __repr__(self):
        return "<Event %r>" % self.Name


class Student(db.Model):
    __tablename__ = "Students"

    StudentID = db.Column(db.String, primary_key=True, unique=True)
    Name = db.Column(db.String, nullable=False)
    Points = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Student %r>" % self.StudentID
