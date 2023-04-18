from flask import Flask, redirect, render_template, request, url_for, flash, session
from datetime import datetime
from models import db, Event, Organization, Student
from forms import LoginForm
from globals import CATEGORIES

# from create_db import make_db
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/RattlersUnite2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "many random bytes"
db.init_app(app)

with app.app_context():
    db.create_all()
    # make_db()

app.jinja_env.globals.update(CATEGORIES=CATEGORIES)


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


def fetch_events(amnt: int = None):
    """
    This function fetches every event and its' information in the
    Events table.

    :param amnt: The amount of events we should fetch at random.
    """
    now = datetime.now()
    query = (
        db.session.query(Event, Organization.Name)
        .join(Organization)
        .filter(Event.Organization == Organization.ID)
    )
    query = query.filter(Event.EndDate > now)

    if amnt:
        # Only return 5 random events that have not ended.
        return query.order_by(func.random()).limit(amnt).all()

    # Return all random events that have not ended.
    return query.all()


def fetch_organizations(amnt: int = None):
    """
    This function fetches the name and ID of every school organization in the
    Organizations table.

    :param amnt: The amount of events we should fetch at random.
    """
    if amnt:
        # Only return 5 random events that have not ended.
        return Organization.query.order_by(func.random()).limit(amnt).all()

    # Return all random events that have not ended.
    return Organization.query.all()


def fetch_leaderboards():
    """
    This function grabs the name and points of every student in the
    Student table.
    """
    return db.session.query(Student.Name, Student.Points).all()


def find_event(id: int):
    """
    This function grabs the event information of a specific event.

    :param id: The ID of the event to look for.
    """
    return Event.query.filter_by(ID=id).first()


def find_organization(id):
    """
    This function grabs the organization information of a specific organization.

    :param id: The ID of the organization to look for.
    """
    return Organization.query.filter_by(ID=id).first()


def list_org_events(org_id):
    """
    This function grabs all the events that a specific organization is hosting.

    :param org_id: The ID of the organization we want events from.
    """
    now = datetime.now()
    query = db.session.query(Event)
    query = query.filter(Event.EndDate > now)
    query = query.filter(Organization.ID == org_id)

    # We will return only events that are after the current local time.
    return query.all()


# signup
def insert_student_data(student_id: str, name: str):
    """
    This function adds new student data into the Students database.

    :param student_id: The ID of the new user.
    :param name: The name of the student
    """
    new_student = Student(StudentID=student_id, Name=name)
    db.session.add(new_student)
    db.session.commit()


# sign in
def fetch_user(student_id: str):
    """
    This function fetches all of the information of one student based off their
    ID number.

    :param student_id: The ID of the user to fetch data from.
    """
    temp = Student.query.filter_by(StudentID=student_id).first()
    print(temp)
    return temp


def getPoints(id: str):
    """
    This function gets the total points a student who is logged in has acumulated.

    :param id: The logged in students' ID number.
    """
    temp = Student.query.filter_by(StudentID=id).first()
    return temp.Points


app.jinja_env.globals.update(getPoints=getPoints)


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


## Site Functions
@app.route("/")
def main():
    events = fetch_events(amnt=5)
    orgs = fetch_organizations(amnt=5)
    a = session.get("username", None)
    # added username if it is in session, unknown if it is not
    return render_template("home.html", events=events, organizations=orgs, name=a)


@app.route("/events")
def events():
    events = fetch_events()
    return render_template("events.html", events=events)


@app.route("/organizations")
def organizations():
    orgs = fetch_organizations()
    return render_template("organizations.html", organizations=orgs)


@app.route("/leaderboards")
def leaderboards():
    board = fetch_leaderboards()
    return render_template("leaderboards.html", board=board)


@app.route("/search/<category>")
def search(category):
    events = fetch_events(True)

    # Crappy for loop check for empty categories but it does it's job IG
    noEvents = True
    for e in events:
        if e["Category"] == category:
            noEvents = False
            break

    return render_template(
        "search.html", events=events, category=category, noEvents=noEvents
    )


@app.route("/eventdetails/<id>")
def eventdetails(id):
    event = find_event(id)
    return render_template("eventPage.html", event=event)


@app.route("/orgdetails/<id>")
def organizationdetails(id):
    org = find_organization(id)
    events = list_org_events(id)
    return render_template("organizationPage.html", org=org, events=events)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        studentID = form.studentID.data
        studentName = form.studentName.data
        user = fetch_user(studentID)
        if user and user.Name == studentName:
            # stores account info
            session["username"] = user.Name
            session["id"] = studentID
            return redirect(url_for("main"))
        else:
            return render_template("LogIn.html", error=True, form=form)
    return render_template("LogIn.html", form=form)


@app.route("/signup")
def signup():
    return render_template("SignUp.html")


@app.route("/orgLogIn")
def orgLogIn():
    return render_template("orgLogIn.html")


# Method to allow user to signup
@app.route("/signupMethod", methods=["GET", "POST"])
def signupMethod():
    if request.method == "POST":
        student_id = request.form["student_id"]
        name = request.form["name"]
        insert_student_data(student_id, name)
        flash("Your account has been created. Please sign in.")
        return redirect(url_for("login"))
    else:
        return render_template("SignUp.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main"))


# @app.route("/add")
# def add_event():
#     form = EventForm()
#     if form.validate_on_submit():
#         conn = connect_db()
#         conn.execute(
#             f"INSERT INTO Events VALUES ({form.eventName}, {session['orgid']}, {form.eventStartDate}, {form.eventEndDate}, {form.eventLocation}, {form.eventDescription}, {form.eventCategory}, {form.eventIcon}, {form.eventBanner})"
#         )
#         conn.commit()
#         return redirect(url_for("main"))
#     return render_template('eventtable.html', form=form)

# @app.route("/edit/<id>")
# def edit_event(id):
#     event = find_event(id)
#     form = EventForm(event[0])

#     if form.validate_on_submit():
#         conn = connect_db()
#         conn.execute(
#             f"INSERT INTO Events VALUES ({form.eventName}, {orgID}, {form.eventStartDate}, {form.eventEndDate}, {form.eventLocation}, {form.eventDescription}, {form.eventCategory}, {form.eventIcon}, {form.eventBanner})"
#         )
#         conn.commit()
#         return redirect(url_for("main"))
#     return render_template('eventtable.html', form=form)



if __name__ == "__main__":
    app.run()
