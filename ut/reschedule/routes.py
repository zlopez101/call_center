from flask import Blueprint, render_template, flash, redirect, url_for
from ut.models import Location, Patient, Appointment, AppointmentSlot
from ut import db
from flask_login import login_required, current_user
from ut.reschedule.utils import create_location_list
from ut.reschedule.forms import SelectApt, FindPatient, PatientData
from ut.public.utils import parse_date_as_string, create_times, create_table_dict
import datetime as dt
import numpy as np


reschedule = Blueprint("reschedule", __name__, template_folder="r_templates")

@reschedule.route("/employee/reschedule",  methods=['GET', 'POST'])
@login_required
def start():
  locations = create_location_list()
  form = FindPatient()
  if form.validate_on_submit():
    flash('Submitted')
    return redirect(url_for('reschedule.find_patient', dob=form.date_of_birth.data.strftime("%m-%d-%Y"), last=form.last.data, first=form.first.data))
  return render_template('start1.html', title='Reschedule', form=form, locations=locations, legend='Find Patient. Date of Birth Required')


@reschedule.route('/employee/reschedule/submit/<string:dob>/<string:first>/<string:last>', methods=['GET', 'POST'])
@login_required
def find_patient(dob, first, last):
  locations = create_location_list()
  _dob = dob.split('-')
  dob_dt = dt.date(int(_dob[2]), int(_dob[0]),int(_dob[1]))
  patients = Patient.query.filter_by(dob=dob_dt,).all()
  if first:
    patients = Patient.query.filter_by(dob=dob_dt,first=first).all()
  if last:
    patients = Patient.query.filter_by(dob=dob_dt,first=first).all()
  if first and last:
    patients = Patient.query.filter_by(dob=dob_dt,first=first, last=last).all()
  return render_template('find_patient2.html', title=f"Choose Correct Patient", patients=patients, locations=locations)

@reschedule.route('/employee/reschedule/patient/<int:patientid>', methods=['GET', 'POST'])
@login_required
def find_appointment(patientid):
  locations = create_location_list()
  patient = Patient.query.filter_by(id=patientid).first()
  appointments = Appointment.query.filter_by(patient_scheduled=patient.id).all()
  return render_template('find_appointment3.html', title=f"Reschedule", locations=locations, appointments=appointments, patient=patient)

@reschedule.route('/employee/reschedule/patient/<int:patientid>/appointment/<int:appointmentid>', methods=['GET', 'POST'])
@login_required
def choose_date(patientid, appointmentid):
  locations = create_location_list()
  patient = Patient.query.filter_by(id=patientid).first()
  appointment = Appointment.query.filter_by(id=appointmentid).first()
  form = SelectApt()
  form.location.choices = [(location.id, location.name) for location in locations]
  if form.validate_on_submit():
      locationid = form.location.data
      _date = form.date.data.replace(year=2020).strftime("%Y-%m-%d")
      return redirect(
          url_for("reschedule.select_time", locationid=locationid, _date=_date, patientid=patient.id, appointmentid=appointment.id)
      )
  return render_template('choose_date4.html', form=form, title=f'Choose new location and date for {patient.first} {patient.last}', legend =f'Choose new location and date for {patient.first} {patient.last}')

@reschedule.route('/employee/reschedule/patient/<int:patientid>/appointment/<int:appointmentid>/date/<string:_date>/<int:locationid>', methods=['GET', 'POST'])
@login_required
def select_time(patientid, appointmentid, _date, locationid):
  locations = create_location_list()
  _date, _ = parse_date_as_string(_date)
  date = dt.datetime.strptime(_date, "%Y-%m-%d")
  appointmentslots = AppointmentSlot.query.filter(
      AppointmentSlot.date_time >= date,
      AppointmentSlot.location_id == locationid,
      AppointmentSlot.date_time < date + dt.timedelta(days=5),
  ).all()
  location = Location.query.filter_by(id=locationid).first_or_404()
  table_dates = np.arange(
      date, date + dt.timedelta(days=5), dtype="datetime64[D]"
  )
  table_times = create_times()
  time_table = create_table_dict(appointmentslots, table_times,table_dates)
  # for table configuration
  table_dates = [
      dt.datetime.strptime(date, "%Y-%m-%d")
      for date in np.datetime_as_string(table_dates)
  ]
  #for side form 
  form = SelectApt()
  form.location.choices = [(location.id, location.name) for location in locations]
  if form.validate_on_submit():
      locationid = form.location.data
      _date = form.date.data.replace(year=2020).strftime("%Y-%m-%d")
      return redirect(
          url_for("reschedule.select_time", locationid=locationid, _date=_date)
      ) 
  return render_template('select_time5.html', title=f"Reschedule", location_id=location.id, form=form, legend = 'Choose another Clinic and Date',
      time_table=time_table,
      dates=table_dates,
      times=table_times,
      request_day=date,
      locations=locations,
      appointmentid=appointmentid,
      patientid=patientid)

@reschedule.route('/employee/reschedule/<int:aS_id>/<int:patientid>/<int:appointmentid>', methods=['GET', 'POST'])
@login_required
def create(aS_id, patientid, appointmentid):
  locations= create_location_list()
  patient = Patient.query.filter_by(id=patientid).first()
  appointment = Appointment.query.filter_by(id=appointmentid).first()
  aS = AppointmentSlot.query.filter_by(id=aS_id).first()
  location = Location.query.filter_by(id=aS.location_id).first()
  title = f"Reschedule {patient.first} {patient.last}'s for {aS.date_time} at {location.name}"
  
  form = PatientData()
  if form.validate_on_submit():
    new_appt = Appointment(created_by=current_user.id, date_created=dt.datetime.utcnow(), patient_scheduled=patient.id, location_id=aS.location_id, status='CONFIRMED', referring_provider=form.referring_provider.data, referral_id=form.referral_number.data, schedule_date_time=aS.date_time)

    db.session.add(new_appt)
    aS.slot_1 = True
    aS.slot_1_appointment = new_appt.id
    appointment.Status = 'CANCELLED'
    db.session.commit()

    flash("Successfully rescheduled an appointment!", 'success')
    return redirect(url_for('employee.e_home'))
  form.first.data = patient.first
  form.last.data = patient.last
  form.date_of_birth.data = patient.dob
  form.language.data = patient.lang
  form.phone_number.data = patient.phone
  form.email.data = patient.email
  
  form.referral_number.data = appointment.referral_id
  form.referring_provider.data = appointment.referring_provider
  side_form = SelectApt()
  side_form.location.choices = [(location.id, location.name) for location in locations]
  side_legend = 'Choose a different location and date'
  if side_form.validate_on_submit():
    
    flash('Choosing a new time and location for {}')
    return redirect(url_for("reschedule.select_time",_date=side_form.date.data.replace(year=2020).strftime("%Y-%m-%d"), appointmentid=appointmentid, locationid=side_form.location.data, patientid=patientid))
  return render_template('create6.html', title=title, form=form, legend=title, locations=locations, side_form=side_form, side_legend=side_legend)



@reschedule.route('/employee/reschedule/creations', methods=['POSTS'])
@login_required
def create_rescheduled_apt():
  flash("Appointment rescheduled!", 'success')
  return redirect(url_for("employee.e_home"))