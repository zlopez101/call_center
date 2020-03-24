from flask_wtf import FlaskForm
from wtforms.fields import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Email, ValidationError
from ut.models import Employee


def ut_email(check="uth.tmc.edu"):
    message = f"Must be a {check} email address"

    def _ut_email(form, field):
        fact = check == field.data.split("@")[-1]
        if not fact:
            raise ValidationError(message)

    return _ut_email

class LoginForm(FlaskForm):
	username = StringField("Username (Your email address)", validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
	first = StringField("First Name", validators=[DataRequired()])
	last = StringField("Last Name", validators=[DataRequired()])
	email = StringField("Email Address", validators=[DataRequired(), Email(), ut_email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Submit')

	'''
	def validate_user(self, username):
		user = Employee.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("That username is taken. Please Choose another.")
	
	def validate_email(self, email):
		user = Employee.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("That email is taken. Please choose a different one.")
	'''
	
class LoginForm_db_not_formed(FlaskForm):
	first = StringField("First Name", validators=[DataRequired()])
	last = PasswordField('Last Name', validators=[DataRequired()])
	submit = SubmitField('Submit')

