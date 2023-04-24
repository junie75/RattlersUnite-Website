from flask import render_template, Blueprint, redirect, url_for, session
from models import Account, OrganizationAccount, db, StudentAccount
from flask_login import current_user, login_user, logout_user
from forms import LoginForm, StudentSignUpForm, OrganizationSignUpForm

login_view = Blueprint('login', __name__)


@login_view.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_view.main"))

    form = LoginForm()
    if form.validate_on_submit():
        user = Account.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("main_view.main"))
        else:
            return render_template("auth/login.html", error=True, form=form)
    return render_template("auth/login.html", form=form)


@login_view.route("/signup", methods=["GET", "POST"])
def signup():
    form = StudentSignUpForm()
    if form.validate_on_submit():
        user = StudentAccount(name=form.name.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login.login"))
    return render_template("auth/signup.html", form=form)


@login_view.route("/orgsignup", methods=["GET", "POST"])
def orgsignup():
    form = OrganizationSignUpForm()
    if form.validate_on_submit():
        user = OrganizationAccount(name=form.name.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login.login"))
    return render_template("auth/orgSignup.html", form=form)


@login_view.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        session.clear()
    return redirect(url_for("main_view.main"))