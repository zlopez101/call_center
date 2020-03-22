from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


class SignUp(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    # Address = StringField("Address", validators=[DataRequired()])
    date_of_birth = DateField("DOB", format="%m/%d/%Y", validators=[DataRequired()])
    """
    martial_status = SelectField(
        "martial status",
        validators=[DataRequired()],
        coerce=int,
        choices=[
            (1, "Single"),
            (2, "Married"),
            (3, "Widowed"),
            (4, "Separated"),
            (5, "Divorced"),
        ],
    )
    ethnicity = SelectField(
        "martial status",
        validators=[DataRequired()],
        coerce=int,
        choices=[
            (1, "Single"),
            (2, "Married"),
            (3, "Widowed"),
            (4, "Separated"),
            (5, "Divorced"),
        ],
    )
    race = SelectField(
        "martial status",
        validators=[DataRequired()],
        coerce=int,
        choices=[
            (1, "Single"),
            (2, "Married"),
            (3, "Widowed"),
            (4, "Separated"),
            (5, "Divorced"),
        ],
    )
    """
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
    # City = StringField("City", validators=[DataRequired()])
    # Zip = StringField("Zip code", validators=[DataRequired()])
    phone_number = StringField("Phone number", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired()])
    submit = SubmitField("Submit")


class CheckApt(FlaskForm):
    date = DateField("Date", format="%m/%d", validators=[DataRequired()])
    submit = SubmitField("Submit")
