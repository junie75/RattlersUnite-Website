from flask import Flask, render_template
import sqlite3

app = Flask(__name__)


def connect_db():
    conn = sqlite3.connect("./db/events.db")
    conn.row_factory = sqlite3.Row
    return conn


def fetch_events():
    conn = connect_db()
    events = conn.execute("SELECT * FROM Events")
    return events.fetchall()


def fetch_organizations():
    conn = connect_db()
    orgs = conn.execute("SELECT * FROM Organizations")
    return orgs.fetchall()


@app.route("/")
def main():
    events = fetch_events()
    orgs = fetch_organizations()
    return render_template("HomePage.html", events=events, organizations=orgs)


@app.route("/events")
def events():
    events = fetch_events()
    return render_template("events.html", events=events, categories=None)


@app.route("/organizations")
def organizations():
    orgs = fetch_organizations()
    return render_template("organizations.html", organizations=orgs)


if __name__ == "__main__":
    app.run()
