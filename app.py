from flask import Flask, redirect, render_template, url_for, session
from datetime import datetime
from models import db, Event, Account, StudentAccount, OrganizationAccount, AdminAccount
from forms import (
    LoginForm,
    StudentSignUpForm,
    OrganizationSignUpForm,
    EventForm,
    OrganizationForm,
)
from globals import CATEGORIES
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
from flask_bcrypt import Bcrypt
from sqlalchemy import func

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../db/RattlersUnite2.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "many random bytes"

login_manager = LoginManager()
login_manager.init_app(app)

bcrypt = Bcrypt(app)

db.init_app(app)

with app.app_context():
    db.create_all()
    # make_db()


@login_manager.user_loader
def load_user(user_id: int):
    user = Account.query.get(user_id)
    if user:
        return user
    return None


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
        db.session.query(Event, OrganizationAccount.name)
        .join(OrganizationAccount)
        .filter(Event.Organization == OrganizationAccount.id)
    )
    query = query.filter(Event.EndDate > now)

    if amnt:
        # Only return 5 random events that have not ended.
        return query.order_by(func.random()).limit(amnt).all()

    # Return all random events that have not ended.
    return query.order_by(Event.StartDate).all()


def fetch_organizations(amnt: int = None):
    """
    This function fetches the name and ID of every school organization in the
    Organizations table.

    :param amnt: The amount of events we should fetch at random.
    """

    if amnt:
        # Only return X random orgs
        return (
            Account.query.filter_by(staff=True)
            .filter_by(admin=False)
            .order_by(func.random())
            .limit(amnt)
            .all()
        )

    # Return all random events that have not ended.
    return Account.query.filter_by(staff=True).filter_by(admin=False).all()


def fetch_leaderboards():
    """
    This function grabs the name and points of every student in the
    Student table.
    """
    return db.session.query(Account.name, Account.points).filter_by(staff=False).order_by(Account.points.desc()).all()


def find_event(id: int):
    """
    This function grabs the event information of a specific event.

    :param id: The ID of the event to look for.
    """
    return Event.query.filter_by(ID=id).first()


def find_profile(id):
    """
    This function grabs the profile information of a specific user/organization.

    :param id: The ID of the organization to look for.
    """
    return Account.query.filter_by(id=id).first()


def list_org_events(org_id):
    """
    This function grabs all the events that a specific organization is hosting.

    :param org_id: The ID of the organization we want events from.
    """
    now = datetime.now()
    query = db.session.query(Event)
    query = query.filter(Event.EndDate > now)
    query = query.filter(Event.Organization == org_id)

    # We will return only events that are after the current local time.
    return query.all()


def fetch_organization(org_id: int):
    """
    This function fetches all of the information of one organization based off their
    ID number.

    :param org_id: The ID of the organization to fetch data from.
    """
    temp = Account.query.filter_by(id=org_id).first()
    return temp


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
    # added username if it is in session, unknown if it is not
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
    print(board)
    return render_template("leaderboards.html", board=board)


@app.route("/search/<category>")
def search(category):
    events = fetch_events()

    # Crappy for loop check for empty categories but it does it's job IG
    noEvents = True
    for e, o in events:
        if e.Category == category:
            noEvents = False
            break

    return render_template(
        "search.html", events=events, category=category, noEvents=noEvents
    )


@app.route("/eventdetails/<id>")
def eventdetails(id):
    event = find_event(id)
    return render_template("eventPage.html", event=event)


@app.route("/profile/<id>")
def profiledetails(id, org=True):
    if org:
        org = find_profile(id)
        events = list_org_events(id)
        return render_template("organizationPage.html", org=org, events=events)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("main"))
        else:
            return render_template("LogIn.html", error=True, form=form)
    return render_template("LogIn.html", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = StudentSignUpForm()
    if form.validate_on_submit():
        user = StudentAccount(name=form.name.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("SignUp.html", form=form)


@app.route("/orgsignup", methods=["GET", "POST"])
def orgsignup():
    form = OrganizationSignUpForm()
    if form.validate_on_submit():
        user = OrganizationAccount(name=form.name.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("OrgSignUp.html", form=form)


@app.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        session.clear()
    return redirect(url_for("main"))


@app.route("/portal")
@login_required
def portal():
    return render_template("orghome.html")


@app.route("/portal/addevent")
def add_event():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.eventName.data,
            organization=current_user.id,
            startDate=form.eventStartDate.data,
            endDate=form.eventEndDate,
            description=form.eventDescription.data,
            category=form.eventCategory.data,
        )
        db.session.add(event)
        db.session.commit()
        return render_template(url_for("portal"))
    return render_template("addevent.html", form=form)


@app.route("/portal/editorg")
def edit_org():
    form = OrganizationForm()
    if form.validate_on_submit():
        org = (
            db.session.query(OrganizationAccount)
            .filter(OrganizationAccount.ID == current_user.id)
            .all()
        )
        org.AboutUs = form.orgDescription.data
        db.session.commit()
        return render_template(url_for("portal"))
    return render_template("editorg.html", form=form)


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
