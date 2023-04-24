from flask import render_template, Blueprint, redirect, url_for, abort
from core import save_image, clean_image_folder
from views import find_event
from flask_login import current_user
from forms import EventForm, OrganizationForm, PointForm
from models import Event, Account, db

admin_view = Blueprint("admin", __name__)


@admin_view.route("/portal")
def portal():
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))

    if not current_user.admin and not current_user.staff:
        abort(403)

    return render_template("admin/orghome.html")


@admin_view.route("/portal/addevent", methods=["GET", "POST"])
def add_event():
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))

    if not current_user.admin and not current_user.staff:
        abort(403)

    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            Name=form.Name.data,
            Organization=current_user.id,
            StartDate=form.StartDate.data,
            EndDate=form.EndDate.data,
            Description=form.Description.data,
            Category=form.Category.data,
        )

        event.EventBanner = save_image(form.EventBanner, "banners")
        event.EventIcon = save_image(form.EventIcon, "icons")

        db.session.add(event)
        db.session.commit()
        return redirect(url_for("admin.portal"))
    return render_template("admin/addevent.html", form=form)


@admin_view.route("/portal/editorg", methods=["GET", "POST"])
def edit_org():
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))

    if not current_user.admin and not current_user.staff:
        abort(403)

    org = Account.query.get(current_user.id)
    form = OrganizationForm(obj=org)

    if form.validate_on_submit():
        if form.icon.data:
            # Delete old banner file
            clean_image_folder(org.icon, False)
            org.icon = save_image(form.icon, "profile_icons")

        form.populate_obj(org)
        db.session.commit()
        return redirect(url_for("admin.portal"))
    return render_template("admin/editorg.html", form=form)


@admin_view.route("/portal/editevent/<id>", methods=["GET", "POST"])
def edit_event(id):
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))

    if not current_user.admin and not current_user.staff:
        abort(403)

    event = find_event(id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        if form.EventBanner.data:
            # Delete old banner file
            clean_image_folder(event.EventBanner)
            event.EventBanner = save_image(form.EventBanner, "banners")

        # Check if new icon was uploaded
        if form.EventIcon.data:
            # Delete old icon file
            clean_image_folder(event.EventIcon, False)
            event.EventIcon = save_image(form.EventIcon, "icons")

        form.populate_obj(event, ignore=["EventIcon", "EventBanner"])
        db.session.commit()
        return redirect(url_for("admin.portal"))
    return render_template("admin/editevent.html", form=form)


@admin_view.route("/portal/addpoints", methods=["GET", "POST"])
def add_points():
    if not current_user.is_authenticated:
        return redirect(url_for("login.login"))

    if not current_user.admin and not current_user.staff:
        abort(403)

    form = PointForm()

    if form.validate_on_submit():
        account = Account.query.filter_by(id=form.student_id.data).first()
        new_points = account.points + form.points.data

        # Make sure no users hit negative
        if new_points < 0:
            account.points = 0
        else:
            account.points = new_points
            
        db.session.commit()
        return redirect(url_for('admin.portal'))

    return render_template("admin/addPoints.html", form=form)