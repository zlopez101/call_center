from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


class SignUp(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    Address = StringField("Address", validators=[DataRequired()])
    Sex = SelectField(
        "Sex",
        validators=[DataRequired()],
        coerce=int,
        choices=[(1, "Male"), (2, "Female"), (3, "Other")],
    )
    date_of_birth = DateField("DOB", validators=[DataRequired()])
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
    language = SelectField(
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
    City = StringField("City", validators=[DataRequired()])
    Zip = StringField("Zip code", validators=[DataRequired()])
    phone_number = StringField("Phone number", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired()])
    submit = SubmitField("Submit")
