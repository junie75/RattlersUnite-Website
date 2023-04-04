from flask import Flask, redirect, render_template, request, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)


## DB Functions
def connect_db():
    """
    This function connects the DB for data access.
    """
    conn = sqlite3.connect("./db/RattlersUnite.db")
    conn.row_factory = sqlite3.Row
    return conn


def sql_time_check(s: list):
    """
    This function removes any event from the provided DB list
    that is before the current date.
    """
    current_date = datetime.now().isoformat()

    for e in s[:]:
        if e["Date"] < current_date:
            s.remove(e)
    return s


def fetch_events(cat=False):
    """
    This function fetches every event and its' information in the
    Events table.

    :param cat: Grabs category from DB for use in category searching
        if set to True.
    """
    conn = connect_db()

    # Grab all info but Category if we are not category searching.
    if not cat:
        events = conn.execute(
            f"SELECT Events.ID, Events.Name, Organizations.Name AS Organization, Date FROM Events JOIN Organizations ON Organizations.ID = Events.Organization ORDER BY Date"
        )
    else:
        events = conn.execute(
            f"SELECT Events.ID, Events.Name, Organizations.Name AS Organization, Date, Category FROM Events JOIN Organizations ON Organizations.ID = Events.Organization ORDER BY Date"
        )

    temp = events.fetchall()

    # We will return only events that are after the current local time.
    return sql_time_check(temp)


def fetch_organizations():
    """
    This function fetches the name and ID of every school organization in the
    Organizations table.
    """
    conn = connect_db()
    orgs = conn.execute("SELECT Name, ID FROM Organizations")
    return orgs.fetchall()


def fetch_leaderboards():
    """
    This function grabs the name and points of every student in the
    Student table.
    """
    conn = connect_db()
    board = conn.execute("SELECT Name, Points FROM Students")
    return board.fetchall()


def find_event(id: int):
    """
    This function grabs the event information of a specific event.

    :param id: The ID of the event to look for.
    """
    conn = connect_db()
    event = conn.execute(
        f"SELECT Events.Name, Organizations.Name AS Organization, Date, Location, Description FROM Events JOIN Organizations ON Organizations.ID = Events.Organization WHERE Events.ID = {id}"
    )
    temp = event.fetchall()

    # Since we are only looking for 1 event by default, we should just
    # return the first and only element
    return temp[0]


def find_organization(id):
    """
    This function grabs the organization information of a specific organization.

    :param id: The ID of the organization to look for.
    """
    conn = connect_db()
    org = conn.execute(
        f"SELECT Name, AboutUs FROM Organizations WHERE Organizations.ID = {id}"
    )
    temp = org.fetchall()

    # Since we are only looking for 1 organization by default, we should just
    # return the first and only element
    return temp[0]


def list_org_events(org_id):
    """
    This function grabs all the events that a specific organization is hosting.

    :param org_id: The ID of the organization we want events from.
    """
    conn = connect_db()
    events = conn.execute(
        f"SELECT Events.ID, Events.Name, Date FROM Events WHERE Events.Organization = {org_id} ORDER BY Date"
    )
    temp = events.fetchall()

    # We will return only events that are after the current local time.
    return sql_time_check(temp)


# signup
def insert_student_data(student_id, name):
    conn = connect_db()
    conn.execute(
        "INSERT INTO Students (StudentID, Name) VALUES (?, ?)", (student_id, name)
    )
    conn.commit()
    conn.close()


# sign in
def fetch_user(student_id):
    conn = connect_db()
    user = conn.execute(
        f"SELECT * FROM Students WHERE StudentID = '{student_id}'"
    ).fetchone()
    return user


def insert_user(student_id, name):
    conn = connect_db()
    conn.execute(
        "INSERT INTO Users (StudentID, Name) VALUES (?, ?)", (student_id, name)
    )
    conn.commit()
    conn.close()


## Filter Functions
@app.template_filter()
def format_datetime(iso: str):
    """
    This function takes a string that is in ISO format and converts it
    to a string in datetime format.

    :param iso: The ISO format string we are converting to datetime.
    """
    dt = datetime.fromisoformat(iso)
    return datetime.strftime(dt, "%B %d, %Y | %I:%M%p CT")


## Site Functions
@app.route("/")
def main():
    events = fetch_events()
    orgs = fetch_organizations()
    return render_template("home.html", events=events, organizations=orgs)


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


@app.route("/login")
def login():
    return render_template("LogIn.html")


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
        return "Data inserted successfully"
    else:
        return render_template("SignUp.html")


# Method to allow user to sign in
@app.route("/loginMethod", methods=["GET", "POST"])
def loginMethod():
    if request.method == "POST":
        student_id = request.form["StudentID"]
        name = request.form["Name"]
        user = fetch_user(student_id)
        if user and user["Name"] == name:
            # authentication succeeded, redirect to main page
            return redirect(url_for("main"))
        else:
            # authentication failed, show error message
            return render_template("login.html", error="Invalid username or password")
    else:
        # display login form
        return render_template("login.html")


if __name__ == "__main__":
    app.run()
