from models import db, Event, Student, Organization
from datetime import datetime, timedelta


def make_db():
    org = Organization(Name="Technical Support Center", AboutUs="Welcome to the TSC!")
    event = Event(
        Name="David's Birthday Party",
        Organization=1,
        StartDate=(datetime.now() + timedelta(5)),
        EndDate=(datetime.now() + timedelta(5, hours=4)),
        Location="Technical Support Center",
        Description="Some tech guy's birthday party.",
        Category="Entertainment",
    )
    student = Student(StudentID="S00693356", Name="Weiss Schnee", Points="9001")

    db.session.add(org)
    db.session.add(event)
    db.session.add(student)
    db.session.commit()
