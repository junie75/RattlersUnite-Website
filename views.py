
from flask import render_template, Blueprint
from models import Event, Account, OrganizationAccount, db
from datetime import datetime
from sqlalchemy import func

main_view = Blueprint('main_view', __name__)


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

## Site Functions
@main_view.route("/")
def main():
    events = fetch_events(amnt=5)
    orgs = fetch_organizations(amnt=5)
    # added username if it is in session, unknown if it is not
    return render_template("home.html", events=events, organizations=orgs)


@main_view.route("/events")
def events():
    events = fetch_events()
    return render_template("sections/events.html", events=events)


@main_view.route("/organizations")
def organizations():
    orgs = fetch_organizations()
    return render_template("sections/organizations.html", organizations=orgs)


@main_view.route("/leaderboards")
def leaderboards():
    board = fetch_leaderboards()
    print(board)
    return render_template("sections/leaderboards.html", board=board)


@main_view.route("/search/<category>")
def search(category):
    events = fetch_events()

    # Crappy for loop check for empty categories but it does it's job IG
    noEvents = True
    for e, o in events:
        if e.Category == category:
            noEvents = False
            break

    return render_template(
        "sections/search.html", events=events, category=category, noEvents=noEvents
    )


@main_view.route("/eventdetails/<id>")
def eventdetails(id):
    event = find_event(id)
    return render_template("pages/eventPage.html", event=event)


@main_view.route("/profile/<id>")
def profiledetails(id, org=True):
    if org:
        org = find_profile(id)
        events = list_org_events(id)
        return render_template("pages/organizationPage.html", org=org, events=events)