from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DateTimeField,
    DateTimeLocalField,
    FileField,
    SubmitField,
    SelectField,
    PasswordField,
    IntegerField,
)
from wtforms.validators import DataRequired, ValidationError, EqualTo
from models import StudentAccount, OrganizationAccount, AdminAccount
from globals import CATEGORIES


# WTForms for login (Student/Organization)
class LoginForm(FlaskForm):
    username = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    password = PasswordField(
        render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    submit = SubmitField("LOGIN")


class AdminLoginForm(FlaskForm):
    username = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    password = PasswordField(
        render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    submit = SubmitField("LOGIN")


# Form for Event Adding/Editing
class EventForm(FlaskForm):
    eventName = StringField("Event Name", validators=[DataRequired()])
    eventLocation = StringField("Event Location", validators=[DataRequired()])
    eventStartDate = DateTimeLocalField("Event Start Date", validators=[DataRequired()])
    eventEndDate = DateTimeLocalField("Event End Date", validators=[DataRequired()])
    eventDescription = TextAreaField("Event Description", validators=[DataRequired()])

    choiceList = [("", "Select a Category")]
    for c in CATEGORIES:
        choiceList.append(c)

    eventCategory = SelectField(
        "Category", validators=[DataRequired()], choices=choiceList
    )

    submit = SubmitField("Submit")


# Form for Organization Description Editing
class OrganizationForm(FlaskForm):
    orgDescription = TextAreaField(
        "Organization Description", validators=[DataRequired()]
    )
    submit = SubmitField("Submit")


class StudentSignUpForm(FlaskForm):
    name = StringField(
        render_kw={"placeholder": "Your name"}, validators=[DataRequired()]
    )
    username = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    password = PasswordField(
        render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        render_kw={"placeholder": "Confirm password"}, validators=[DataRequired()]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = StudentAccount.get_by_username(username.data)
        if user:
            print("AAA")
            raise ValidationError("Username already exists.")

    def validate_confirm_password(form, field):
        if form.password.data != field.data:
            raise ValidationError("Passwords do not match.")


class OrganizationSignUpForm(FlaskForm):
    name = StringField(
        render_kw={"placeholder": "Your organization name"}, validators=[DataRequired()]
    )
    username = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    password = PasswordField(
        render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        render_kw={"placeholder": "Confirm password"}, validators=[DataRequired()]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = OrganizationAccount.get_by_username(username.data)
        if user:
            raise ValidationError("Username already exists.")

    def validate_confirm_password(form, field):
        if form.password.data != field.data:
            raise ValidationError("Passwords do not match.")


class AdminSignUpForm(FlaskForm):
    name = StringField(
        render_kw={"placeholder": "Your name"}, validators=[DataRequired()]
    )
    username = StringField(
        render_kw={"placeholder": "Username"}, validators=[DataRequired()]
    )
    password = PasswordField(
        render_kw={"placeholder": "Password"}, validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        render_kw={"placeholder": "Confirm password"}, validators=[DataRequired()]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = AdminAccount.get_by_username(username.data)
        if user:
            raise ValidationError("Username already exists.")

    def validate_confirm_password(form, field):
        if form.password.data != field.data:
            raise ValidationError("Passwords do not match.")
