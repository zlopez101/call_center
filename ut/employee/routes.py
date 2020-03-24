from flask import render_template, Blueprint, flash, redirect, url_for, request
from ut.employee.forms import RegisterForm, LoginForm_db_not_formed
from flask_login import current_user, login_required, login_user, logout_user
from ut.models import Employee, Location, AppointmentSlot, Patient, Appointment
from ut.public.forms import SignUp, CheckApt
from ut.public.utils import parse_date_as_string, create_times, create_table_dict
from ut import db
import datetime as dt
import numpy as np


employee = Blueprint("employee", __name__, template_folder="employee_templates")

@employee.route('/employee_home', methods=["GET", "POST"])
@login_required
def home():
	locations = Location.query.all()
	form=SignUp()
	if form.validate_on_submit():
		flash("Form Submission was complete!", "success")
	return render_template('e_home.html', title='UT Physicians Employee Home Page', locations=locations, form=form, legend="Sign Up Caller Now")

@employee.route('/location/<int:locationid>', methods=["GET", "POST"])
@login_required
def location(locationid):
	locations = Location.query.all()
	_location = Location.query.filter_by(id=locationid).first()
	form = CheckApt()
	if form.validate_on_submit():
		flash(f"{_location.name} schedule for next five days after your chosen date {form.date.data.strftime('%m/%d')}", "success")
		_date = form.date.data.replace(2020)
		date_and_time = dt.datetime.combine(_date, dt.time(hour=8, minute=0, second=0))
		return redirect(url_for("employee.locationwithdate", locationid=_location.id, date=date_and_time))
	return render_template('e_location.html', title=f"{_location.name} Appointments", location=_location, locations=locations, form=form)


@employee.route("/location/<int:locationid>/date/<string:date>", methods=["GET", "POST"])
@login_required
def locationwithdate(locationid, date):
	locations = Location.query.all()
	location = Location.query.filter_by(id=locationid).first()
	_date, _ = parse_date_as_string(date)
	date = dt.datetime.strptime(_date, "%Y-%m-%d")
	appointmentslots = AppointmentSlot.query.filter(AppointmentSlot.date_time >= date, AppointmentSlot.location_id == locationid,AppointmentSlot.date_time < date + dt.timedelta(days=5)).all()
	table_dates = np.arange(date, date + dt.timedelta(days=5), dtype="datetime64[D]")
	table_times = create_times()
	time_table = create_table_dict(appointmentslots, table_times, table_dates)
	return render_template("e_locationwithdate.html",title=f"{location.name} on {_date} appointments",legend=f"{location.name} on {_date} appointments. Submit Form to sign into an appointment.", location_id=location.id, time_table=time_table, dates=table_dates, times=table_times, request_day=date, locations=locations)

@employee.route("/location/<int:locationid>/date/<string:date>/create_appointment<int:aS_id>", methods=["GET", "POST"])
@login_required
def appointment(locationid, date, aS_id):
	locations = Location.query.all()
	aS = AppointmentSlot.query.filter_by(id=aS_id).first()
	location = Location.query.filter_by(id=locationid).first()
	request_date_as_datetime = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
	_day, _time = parse_date_as_string(date)
	form = SignUp()
	if form.validate_on_submit():
		'Creating new patients'
		new_patient = Patient(first=form.first_name.data, last=form.last_name.data, dob=form.date_of_birth.data, phone=form.phone_number.data,email=form.email.data, lang=form.language.data,)
		db.session.add(new_patient)
		aS.slot_1 = True
		db.session.commit()

		"Create the new Appointment"
		web_employee = Employee.query.filter_by(first='Web').first()
		new_appointment = Appointment(created_by=web_employee.id, date_created=dt.datetime.utcnow(), patient_scheduled=new_patient.id, location_id=locationid,schedule_date_time=request_date_as_datetime, status="PENDING")
		db.session.add(new_appointment)
		db.session.commit()
		flash(f"{new_patient.first} {new_patient.last} created an appointment at {location.name} on {_day} at {_time}. Thank you", "success",)
		return redirect(url_for("confirmations.confirm_appointment",locationid=locationid,date=date,patientid=new_patient.id,))
	return render_template("e_appointment.html",title="Sign up Today",legend=f"Sign Up for an Appointment on {_day} at {_time} at {location.name}.",form=form, locations=locations)



@employee.route('/login', methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for("main_blueprint.home"))
	form = LoginForm_db_not_formed()
	if form.validate_on_submit():

		employee = Employee.query.filter_by(last=form.last.data).first()
		if employee:
			login_user(employee)
			next_page = request.args.get("next")
			return redirect(next_page) if next_page else redirect(url_for("employee.home"))
		else:
			flash("Login Unsuccessful", "danger")
	return render_template('login.html', title='Login', form=form, legend='Login')

@employee.route('/register', methods=["GET", "POST"])
def register():
	form = RegisterForm()
	if form.validate_on_submit():
		new_emp = Employee(first=form.first.data, last=form.last.data)
		db.session.add(new_emp)
		db.session.commit()
		flash('you registered!', 'success')
		return redirect(url_for('employee.login'))
	return render_template('register.html', title='Registration Page', form=form, legend='Register')

@employee.route('/logout', methods=["GET", 'POST'])
@login_required
def logout():
	logout_user()
	return redirect(url_for("employee.login"))

@employee.route('/about')
@login_required
def about():
	return render_template('e_about.html')
