from flask import Flask, render_template
from datetime import datetime
import sqlite3

app = Flask(__name__)

## DB Functions
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

def fetch_leaderboards():
    conn = connect_db()
    board = conn.execute("SELECT * FROM Leaderboards")
    return board.fetchall()

## Filter Functions
@app.template_filter()
def format_datetime(iso):
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
    return render_template("events.html", events=events, categories=None)


@app.route("/organizations")
def organizations():
    orgs = fetch_organizations()
    return render_template("organizations.html", organizations=orgs)

@app.route("/leaderboards")
def leaderboards():
    board = fetch_leaderboards()
    return render_template("leaderboards.html", board=board)

if __name__ == "__main__":
    app.run()
