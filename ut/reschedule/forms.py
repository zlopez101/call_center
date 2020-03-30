from flask_wtf import FlaskForm
from wtforms.fields import (
    StringField,
    SubmitField,
    SelectField,
    DateField,
    DateTimeField,
    BooleanField
)
from wtforms.validators import DataRequired

class SelectApt(FlaskForm):
    location = SelectField("Location", coerce=int)
    date = DateField("Date", format="%m/%d", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class FindPatient(FlaskForm):
  first = StringField("First Name")
  last = StringField('Last Name')
  date_of_birth = DateField('Date as MM/DD/YYYY', format="%m/%d/%Y", validators=[DataRequired()])
  submit=SubmitField('Submit')

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
    referring_provider = StringField("Referring Provider")
    referral_number = StringField("Referral Number")
    submit = SubmitField("Submit")