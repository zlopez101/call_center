from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
    PasswordField,
    SelectField,
    DateField,
    DateTimeField,
    BooleanField,
    TextAreaField,
)
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from ut.models import Employee
from datetime import datetime


def ut_email(check="uth.tmc.edu"):
    message = f"Must be a {check} email address"

    def _ut_email(form, field):
        fact = check == field.data.split("@")[-1]
        if not fact:
            raise ValidationError(message)

    return _ut_email


class LoginForm(FlaskForm):
    username = StringField("Username (Your email address)", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    first = StringField("First Name", validators=[DataRequired()])
    last = StringField("Last Name", validators=[DataRequired()])
    email = StringField(
        "Email Address", validators=[DataRequired(), Email(), ut_email()]
    )
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Submit")

    """
  def validate_user(self, username):
    user = Employee.query.filter_by(username=username.data).first()
    if user:
      raise ValidationError("That username is taken. Please Choose another.")
  
  def validate_email(self, email):
    user = Employee.query.filter_by(email=email.data).first()
    if user:
      raise ValidationError("That email is taken. Please choose a different one.")
  """


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class SelectApt(FlaskForm):
    location = SelectField("Location", coerce=int)
    date = DateField("Date", format="%m/%d", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PatientData(FlaskForm):
    first = StringField("First Name", validators=[DataRequired()])
    last = StringField("Last Name", validators=[DataRequired()])
    date_of_birth = DateField("DOB", format="%m/%d/%Y", validators=[DataRequired()])
    language = SelectField(
        "Language",
        validators=[DataRequired()],
        coerce=int,
        choices=[
            (1, "English"),
            (2, "Spanish"),
            (3, "French"),
            (4, "Chinese"),
            (5, "Korean"),
        ],
    )
    phone_number = StringField("Phone number", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired()])
    verified_pt = SelectField("Patient is verified?", coerce=int, validators=[DataRequired()])
    verified_appt = SelectField("Appointment Status", coerce=int, validators=[DataRequired()])
    referring_provider = StringField("Referring Provider")
    referral_number = StringField("Referral Number")
    appointment_time = DateTimeField("Appointment Time")
    appointment_location = SelectField("Location", coerce=int)
    submit = SubmitField("Submit")

class IssueSubmit(FlaskForm):
  title = StringField("What's the problem?", validators=[DataRequired()])
  descript = TextAreaField('Please describe in detail', validators=[DataRequired()])
  submit = SubmitField("Submit")

class FindPatient(FlaskForm):
  first = StringField("First Name")
  last = StringField('Last Name')
  date_of_birth = DateField('Date as MM/DD/YYYY', format="%m/%d/%Y", validators=[DataRequired()])
  submit=SubmitField('Submit')