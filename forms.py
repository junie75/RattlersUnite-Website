from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DateTimeLocalField,
    FileField,
    SubmitField,
    SelectField,
    PasswordField,
    DateTimeLocalField,
)
from flask_wtf.file import FileAllowed
from wtforms.validators import DataRequired, ValidationError
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
    Name = StringField("Event Name", validators=[DataRequired()])
    Location = StringField("Event Location", validators=[DataRequired()])
    StartDate = DateTimeLocalField(
        "Event Start Date/Time", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    EndDate = DateTimeLocalField(
        "Event End Date", format="%Y-%m-%dT%H:%M", validators=[DataRequired()]
    )
    Description = TextAreaField("Event Description", validators=[DataRequired()])
    EventIcon = FileField(
        "Event Icon Image",
        validators=[FileAllowed(["jpg", "png"], "Only JPGs or PNGs are supported.")],
    )
    EventBanner = FileField(
        "Event Banner Image",
        validators=[FileAllowed(["jpg", "png"], "Only JPGs or PNGs are supported.")],
    )

    choiceList = [("", "Select a Category")]
    for c in CATEGORIES:
        choiceList.append(c)

    Category = SelectField("Category", validators=[DataRequired()], choices=choiceList)

    submit = SubmitField("Submit")

    def validate(self, extra_validators=None):
        if not FlaskForm.validate(self):
            return False

        if self.EndDate.data < self.StartDate.data:
            self.EndDate.errors.append("End Date must be greater than Start Date")
            return False

        return True

    def populate_obj(self, obj, ignore=[]):
        """
        Populates the attributes of the passed `obj` with data from the form's
        fields, ignoring disabled fields.
        """
        for name, field in self._fields.items():
            if name not in ignore:
                field.populate_obj(obj, name)


# Form for Organization Description Editing
class OrganizationForm(FlaskForm):
    about = TextAreaField("Organization Description", validators=[DataRequired()])
    icon = FileField(
        "Profile Image",
        validators=[FileAllowed(["jpg", "png"], "Only JPGs or PNGs are supported.")],
    )
    submit = SubmitField("Submit")

    def populate_obj(self, obj, ignore=["icon"]):
        """
        Populates the attributes of the passed `obj` with data from the form's
        fields, ignoring disabled fields.
        """
        for name, field in self._fields.items():
            if name not in ignore:
                field.populate_obj(obj, name)


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
