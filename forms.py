
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    DateTimeField,
    FileField,
    SubmitField,
    SelectField,
)
from wtforms.validators import DataRequired
from globals import CATEGORIES

class LoginForm(FlaskForm):
    studentID = StringField(render_kw={"placeholder": "Student ID i.e. S00123456"}, validators=[DataRequired()])
    studentName = StringField(render_kw={"placeholder": "Student Name"}, validators=[DataRequired()])
    submit = SubmitField("Login")


# Form for Event Adding/Editing
class EventForm(FlaskForm):
    eventName = StringField("Event Name", DataRequired())
    eventLocation = StringField("Event Location", DataRequired())
    eventStartDate = DateTimeField("Event Start Date", DataRequired())
    eventEndDate = DateTimeField("Event End Date", DataRequired())
    eventDescription = TextAreaField("Event Description", DataRequired())

    choiceList = [("", "Select a Category")]
    for c in CATEGORIES:
        choiceList.append(c)

    eventCategory = SelectField("Category", DataRequired(), choices=choiceList)

    submit = SubmitField("Submit")


# Form for Organization Description Editing
class OrganizationForm(FlaskForm):
    orgDescription = TextAreaField("Organization Description", DataRequired())
    submit = SubmitField("Submit")