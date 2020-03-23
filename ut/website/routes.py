from flask import render_template, Blueprint, flash, redirect, url_for
from ut.models import Location, Appointment, Patient, Employee, AppointmentSlot
from ut.website.forms import SignUp, CheckApt
from ut.website.utils import build_times
from ut import db
import datetime
import numpy as np


website = Blueprint("website", __name__)

@website.route("/")
def home():
    locations = Location.query.all()
    return render_template("welcome.html", locations=locations)


@website.route("/<int:locationid>", methods=["GET", "POST"])
def samplelocation(locationid):
	appointments_at_location = Appointment.query.filter_by(location_id=locationid).all()
	location = Location.query.filter_by(id=locationid).first_or_404()
	
	form = CheckApt()
	if form.validate_on_submit():
		flash("We submitted a form", "success")
		date= form.date.data
		date = date.replace(2020)
		date_and_time = datetime.datetime.combine(date, datetime.time(hour=8, minute=0, second=0))
		print(type(date_and_time))
		print(date_and_time)
		return redirect(url_for("website.samplelocation_with_date",locationid=location.id,date=date_and_time))
	return render_template("location.html",title="title",appointments=appointments_at_location,location=location,form=form,legend="Pick a date to check appointment availability",)


@website.route("/<int:locationid>/<string:date>", methods=["GET", "POST"])
def samplelocation_with_date(locationid, date):

	date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

	appointmentslots = AppointmentSlot.query.filter(AppointmentSlot.date_time>=date, AppointmentSlot.location_id==locationid, AppointmentSlot.date_time<date + datetime.timedelta(days=5)).all()

	location = Location.query.filter_by(id=locationid).first_or_404()

	table_dates = np.arange(date, date + datetime.timedelta(days=5), dtype="datetime64[D]")

	#define times
	def create_times():
		time_start = datetime.datetime.strptime("08:00:00", "%H:%M:%S")
		times = []
		times.append(time_start)
		i = 0
		while i < 36:
			time_start = time_start+datetime.timedelta(minutes=15)
			times.append(time_start)
			i = i+1
		
		return times
	table_times = create_times()
	datetime_dct = build_times()

	time_table = {}
	#match appointment to their time and date
	for date in table_dates:
		for time in table_times:
			time_table[time] = [aS for aS in appointmentslots if aS.date_time.strftime("%Y-%m-%d %H:%M").split(' ')[-1]==time.strftime('%H:%M')]

	
	print(type((appointmentslots[1].date_time.strftime("%m/%d, %H:%M"))))
			

	form = SignUp()
	if form.validate_on_submit():
		flash("Still got it!")
	return render_template("appointment.html",title=f"{location.name} on {date} appointments",legend=f"{location.name} on {date} appointments. Submit Form to sign into an appointment.",location_id=location.id,form=form,time_table=time_table,dates=table_dates, times=table_times, request_day=date, datetime_dct=datetime_dct)


@website.route(
    "/my_appointment/<int:locationid>/<string:date>/<string:request_time>/<int:aS_id>",
    methods=["GET", "POST"],
)
def my_appointment(locationid, date, request_time, aS_id):
	aS = AppointmentSlot.query.filter_by(id=aS_id).first()
	location = Location.query.filter_by(id=locationid).first()
	date = datetime.datetime.strptime(date, "%Y-%m-%d")
	print(request_time)
	request_time = request_time.split(' ')[-1]
	timing = request_time.split(':')
	print(timing)
	r_time = datetime.datetime.strptime(request_time, "%H:%M:%S")
	print(r_time)
	form=SignUp()
	print(date)
	
	if form.validate_on_submit():
		"Creating the new patient"
		new_patient=Patient(first=form.first_name.data,last=form.last_name.data, dob=form.date_of_birth.data, phone=form.phone_number.data, email=form.email.data, lang=form.language.data)
		db.session.add(new_patient)
		aS.slot_1=True
		db.session.commit()

		"Creating the new Appointment"
		web_employee = Employee.query.filter_by(first='Zachary').first()
		new_appointment = Appointment(created_by=web_employee.id, date_created=datetime.datetime.utcnow(), patient_scheduled=new_patient.id, location_id=locationid, schedule_date_time=date, status='PENDING')
		db.session.add(new_appointment)
		db.session.commit()

		flash(f"{new_patient.first} {new_patient.last} created an appointment at {location.name} on {new_appointment.schedule_date_time}. Thank you ")
		return redirect(url_for("website.samplelocation_with_date", locationid=locationid,date=date))
	return render_template("my_appointment.html", title="Sign up Today", legend=f"Sign Up forappointment on {date} at {request_time} at {locationid}.", form=form)