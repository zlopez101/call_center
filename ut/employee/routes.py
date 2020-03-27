from flask import (
    render_template,
    Blueprint,
    flash,
    redirect,
    url_for,
    request,
    current_app,
)
from ut.employee.forms import (
    RegisterForm,
    LoginForm,
    SelectApt,
    PatientData,
    IssueSubmit,
    FindPatient
)
from ut.employee.utils import create_location_list
from flask_login import current_user, login_required, login_user, logout_user
from ut.models import Employee, Location, AppointmentSlot, Patient, Appointment
from ut.public.forms import SignUp, CheckApt
from ut.public.utils import parse_date_as_string, create_times, create_table_dict
from ut import db, bcrypt
import datetime as dt
import numpy as np


employee = Blueprint("employee", __name__, template_folder="employee_templates")


@employee.route("/employee_home", methods=["GET", "POST"])
@login_required
def e_home():
    "The employee home page"
    locations = create_location_list()
    form = SignUp()
    if form.validate_on_submit():
        flash("Form Submission was complete!", "success")
    return render_template(
        "main/e_home.html",
        title="UT Physicians Employee Home Page",
        locations=locations,
        form=form,
        legend="Sign Up Caller Now",
    )


@employee.route("/employee/selectapt", methods=["GET", "POST"])
@login_required
def selectapt():
    locations = create_location_list()
    form = SelectApt()
    form.location.choices = [(location.id, location.name) for location in locations]
    if form.validate_on_submit():
        locationid = form.location.data
        _date = form.date.data.replace(year=2020).strftime("%Y-%m-%d")
        return redirect(
            url_for("employee.pending_appointments", locationid=locationid, _date=_date)
        )

    return render_template(
        "e_select_appt.html",
        title="Sort appointments by location and date",
        form=form,
        legend="Select Location and Date for appointments",
        locations=locations,
    )


@employee.route(
    "/employee/pendingappointments/<int:locationid>/<string:_date>",
    methods=["GET", "POST"],
)
@login_required
def pending_appointments(locationid, _date):
    beginning_of_date = dt.datetime.strptime(_date, "%Y-%m-%d").replace(year=2020)
    end_of_date = dt.datetime(
        beginning_of_date.year, beginning_of_date.month, beginning_of_date.day, 18
    )
    locations = create_location_list()
    loc = Location.query.filter_by(id=locationid).first()
    appointments = Appointment.query.filter(
        Appointment.location_id == loc.id,
        Appointment.schedule_date_time > beginning_of_date,
        Appointment.schedule_date_time < end_of_date,
        Appointment.status != "Status.CANCELLED"
    ).all()
    patients = (
        Patient.query.join(Appointment)
        .filter(
            Appointment.location_id == loc.id,
            Appointment.schedule_date_time > beginning_of_date,
            Appointment.schedule_date_time < end_of_date,
            Appointment.status != "Status.CANCELLED"
        )
        .all()
    )
    appointment_with_patient = zip(appointments, patients)

    form = SelectApt()
    form.location.choices = [(location.id, location.name) for location in locations]
    if form.validate_on_submit():
        locationid = form.location.data
        _date = form.date.data.strftime("%Y-%m-%d")
        return redirect(
            url_for("employee.pending_appointments", locationid=locationid, _date=_date)
        )
    return render_template(
        "e_pendingappt.html",
        title="Patients needing confirmations",
        _date=_date,
        loc=loc,
        appointment_with_patient=appointment_with_patient,
        locations=locations,
        form=form,
        legend="Select New Location and Date for appointments",
    )


@employee.route(
    "/employee/patient_inquiry/<int:appointmentid>/<int:locationid>/<string:_date>",
    methods=["GET", "POST"],
)
@login_required
def patient_inquiry(appointmentid, locationid, _date):
    locations = create_location_list()
    location= Location.query.filter_by(id=locationid).first()
    appointment = Appointment.query.filter_by(id=appointmentid).first()
    patient = Patient.query.filter_by(id=appointment.patient_scheduled).first()
    form = PatientData()
    ls = ["Pending",  "Confirmed"]
    ls1 = ['PENDING',  "CONFIRMED"]
    form.appointment_location.choices = [
        (location.id, location.name) for location in locations
    ]
    form.verified_appt.choices = [(i, status) for i, status in enumerate(ls)]
    form.verified_pt.choices = [(1, True), (2, False)]
    if form.validate_on_submit():
        patient.first= form.first.data
        patient.last=  form.last.data
        patient.dob = form.date_of_birth.data
        patient.phone=  form.phone_number.data
        patient.email =  form.email.data
        patient.lang=  form.language.data
        patient.confirmed =  form.verified_pt.data
        appointment.status = ls1[form.verified_appt.data]
        appointment.referring_provider=  form.referring_provider.data
        appointment.referral_id = form.referral_number.data
        appointment.schedule_date_time=  form.appointment_time.data
        db.session.commit()       
        flash(
            f"Succesfully updated {patient.first} {patient.last}'s appointment. Thanks for your hard work!",
            "success",
        )
        return redirect(
            url_for("employee.pending_appointments", locationid=locationid, _date=_date)
        )
    form.first.data = patient.first
    form.last.data = patient.last
    form.date_of_birth.data = patient.dob
    form.phone_number.data = patient.phone
    form.email.data = patient.email
    form.language.data = patient.lang
    form.verified_pt.data = patient.confirmed
    form.referring_provider.data = appointment.referring_provider
    form.referral_number.data = appointment.referral_id
    form.appointment_location.data = (
        Location.query.filter_by(id=locationid).first().name
    )
    form.appointment_time.data = appointment.schedule_date_time
    side_form = SelectApt()
    side_form.location.choices = [
        (location.id, location.name) for location in locations
    ]
    if side_form.validate_on_submit():
        locationid = side_form.location.data
        _date = side_form.date.data.strftime("%Y-%m-%d")
        return redirect(
            url_for("employee.pending_appointments", locationid=locationid, _date=_date)
        )
    return render_template(
        "patient.html",
        title="Patient Inquiry",
        locations=locations,
        appointmentid =appointment.id,
        location=location.id,
        _date=_date,
        form=form,
        legend=f"{patient.first} {patient.last}",
        side_form=side_form,
        side_legend="Choose a different appointment table.",
    )

@employee.route("/employee/patient_inquiry/delete/<int:appointmentid>/<int:locationid>/<string:_date>", methods=['POST'])
@login_required
def delete_appointment(appointmentid, locationid, _date):
  appointment = Appointment.query.filter_by(id=appointmentid).first()
  print(appointment)
  aS = AppointmentSlot.query.filter_by(slot_1_appointment=appointment.id).first()
  appointment.status = 'CANCELLED'
  print(aS)
  aS.slot_1 = False
  aS.slot_1_appointment = None
  db.session.commit()
  flash(f"{appointment.id} deleted, {appointment.status}", 'info')
  return redirect(
            url_for("employee.pending_appointments", locationid=locationid, _date=_date)
        )

@employee.route("/location/<int:locationid>", methods=["GET", "POST"])
@login_required
def location(locationid):
    locations = create_location_list()
    _location = Location.query.filter_by(id=locationid).first()
    form = CheckApt()
    if form.validate_on_submit():
        flash(
            f"{_location.name} schedule for next five days after your chosen date {form.date.data.strftime('%m/%d')}",
            "success",
        )
        _date = form.date.data.replace(2020)
        date_and_time = dt.datetime.combine(_date, dt.time(hour=8, minute=0, second=0))
        return redirect(
            url_for(
                "employee.locationwithdate", locationid=_location.id, date=date_and_time
            )
        )
    return render_template(
        "e_location.html",
        title=f"{_location.name} Appointments",
        location=_location,
        locations=locations,
        form=form,
    )

@employee.route(
    "/location/<int:locationid>/date/<string:date>", methods=["GET", "POST"]
)
@login_required
def locationwithdate(locationid, date):
    locations = create_location_list()
    location = Location.query.filter_by(id=locationid).first()
    _date, _ = parse_date_as_string(date)
    date = dt.datetime.strptime(_date, "%Y-%m-%d")
    appointmentslots = AppointmentSlot.query.filter(
        AppointmentSlot.date_time >= date,
        AppointmentSlot.location_id == locationid,
        AppointmentSlot.date_time < date + dt.timedelta(days=5),
    ).all()
    table_dates = np.arange(date, date + dt.timedelta(days=5), dtype="datetime64[D]")
    table_times = create_times()
    time_table = create_table_dict(appointmentslots, table_times, table_dates)
    return render_template(
        "e_locationwithdate.html",
        title=f"{location.name} on {_date} appointments",
        legend=f"{location.name} on {_date} appointments. Submit Form to sign into an appointment.",
        location_id=location.id,
        time_table=time_table,
        dates=table_dates,
        times=table_times,
        request_day=date,
        locations=locations,
    )

@employee.route(
    "/location/<int:locationid>/date/<string:date>/create_appointment<int:aS_id>",
    methods=["GET", "POST"],
)
@login_required
def appointment(locationid, date, aS_id):
    locations = create_location_list()
    aS = AppointmentSlot.query.filter_by(id=aS_id).first()
    location = Location.query.filter_by(id=locationid).first()
    request_date_as_datetime = dt.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    _day, _time = parse_date_as_string(date)
    form = SignUp()
    if form.validate_on_submit():
        "Creating new patients"
        new_patient = Patient(
            first=form.first_name.data,
            last=form.last_name.data,
            dob=form.date_of_birth.data,
            phone=form.phone_number.data,
            email=form.email.data,
            lang=form.language.data,
        )
        db.session.add(new_patient)
        aS.slot_1 = True
        db.session.commit()

        "Create the new Appointment"
        web_employee = Employee.query.filter_by(first="Web").first()
        new_appointment = Appointment(
            created_by=web_employee.id,
            date_created=dt.datetime.utcnow(),
            patient_scheduled=new_patient.id,
            location_id=locationid,
            schedule_date_time=request_date_as_datetime,
            status="PENDING",
        )
        db.session.add(new_appointment)
        db.session.commit()
        flash(
            f"{new_patient.first} {new_patient.last} created an appointment at {location.name} on {_day} at {_time}. Thank you",
            "success",
        )
        return redirect(
            url_for(
                "confirmations.confirm_appointment",
                locationid=locationid,
                date=date,
                patientid=new_patient.id,
                _from="employee",
            )
        )
    return render_template(
        "e_appointment.html",
        title="Sign up Today",
        legend=f"Sign Up for an Appointment on {_day} at {_time} at {location.name}.",
        form=form,
        locations=locations,
    )

@employee.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("employee.e_home"))
    form = LoginForm()
    if form.validate_on_submit():
      employee = Employee.query.filter_by(username=form.username.data).first()
      if employee and bcrypt.check_password_hash(employee.password, form.password.data):
          login_user(employee)
          next_page = request.args.get("next")
          employee.is_active = True
          db.session.commit()
          return (
              redirect(next_page)
              if next_page
              else redirect(url_for("employee.e_home"))
          )
      else:
          flash("Login Unsuccessful", "danger")
    return render_template("main/login.html", title="Login", form=form, legend="Login")

@employee.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
      hash_pass = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
      new_emp = Employee(first=form.first.data, last=form.last.data,email=form.email.data,username=form.username.data, password=hash_pass)
      db.session.add(new_emp)
      db.session.commit()
      flash("you registered!", "success")
      return redirect(url_for("employee.login"))
    return render_template("main/register.html", title="Registration Page", form=form, legend="Register")

@employee.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logging_out_employee = Employee.query.filter_by(id=current_user.id).first()
    logging_out_employee.is_active = False
    db.session.commit()
    logout_user()
    return redirect(url_for("employee.login"))

@employee.route("/employee/about")
@login_required
def e_about():
  locations = create_location_list()
  return render_template("main/e_about.html", title='About Page', locations = locations)

@employee.route("/employee/team")
@login_required
def team():
  locations = create_location_list()
  employees = Employee.query.all()
  return render_template('main/team.html', title='Meet the Team', employees=employees, locations=locations)

@employee.route("/employee/profile/<int:employeeid>")
@login_required
def profile(employeeid):
  locations = create_location_list()
  employee = Employee.query.filter_by(id=employeeid).first()
  form = RegisterForm()
  if form.validate_on_submit():
    hash_pass = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
    employee.first = form.first.data
    employee.last = form.last.data
    employee.username = form.use.data
    employee.email = form.email.data
    employee.password = hash_pass
    db.session.commit()
  form.first.data = employee.first
  form.last.data = employee.data
  form.email.data = employee.email
  form.username.data = employee.username
  return render_template('profile.html', title=f'{employee.first} {employee.last} profile', form=form, locations=locations)

@employee.route("/employee/issue_submit", methods=['GET', 'POST'])
@login_required
def issue_submit():
  locations = create_location_list()
  form = IssueSubmit()
  if form.validate_on_submit():
    flash("Thanks for your input!", "success")
  return render_template('main/issue_submission.html', title='Submit an issue', locations=locations)


@employee.route("/employee/reschedule",  methods=['GET', 'POST'])
@login_required
def reschedule():
  locations = create_location_list()
  form = FindPatient()
  if form.validate_on_submit():
    flash('Submitted')
    return redirect(url_for('employee.find_patient', dob=form.date_of_birth.data.strftime("%m-%d-%Y"), last=form.last.data, first=form.first.data))
  return render_template('reschedule/start.html', title='Reschedule', form=form, locations=locations, legend='Find Patient. Date of Birth Required')


@employee.route('/employee/reschedule/submit/<string:dob>/<string:first>/<string:last>', methods=['GET', 'POST'])
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
  return render_template('reschedule/find_patient.html', title=f"Choose Correct Patient", patients=patients, locations=locations)

@employee.route('/employee/reschedule/patient/<int:patientid>', methods=['GET', 'POST'])
@login_required
def reschedule_patient(patientid):
  locations = create_location_list()
  patient = Patient.query.filter_by(id=patientid).first()
  appointments = Appointment.query.filter_by(patient_scheduled=patient.id).all()
  return render_template('reschedule/find_appointment.html', title=f"Reschedule", locations=locations, appointments=appointments, patient=patient)

@employee.route('/employee/reschedule/patient/<int:patientid>/appointment/<int:appointmentid>', methods=['GET', 'POST'])
@login_required
def reschedule_choose_date(patientid, appointmentid):
  locations = create_location_list()
  patient = Patient.query.filter_by(id=patientid).first()
  appointment = Appointment.query.filter_by(id=appointmentid).first()
  form = SelectApt()
  form.location.choices = [(location.id, location.name) for location in locations]
  if form.validate_on_submit():
      locationid = form.location.data
      _date = form.date.data.replace(year=2020).strftime("%Y-%m-%d")
      return redirect(
          url_for("employee.reschedule_patient_appointment", locationid=locationid, _date=_date, patientid=patient.id, appointmentid=appointment.id)
      )
  return render_template('reschedule/choose.html', form=form, title=f'Choose new location and date for {patient.first} {patient.last}', legend =f'Choose new location and date for {patient.first} {patient.last}')

@employee.route('/employee/reschedule/patient/<int:patientid>/appointment/<int:appointmentid>/date/<string:_date>/<int:locationid>', methods=['GET', 'POST'])
@login_required
def reschedule_patient_appointment(patientid, appointmentid, _date, locationid):
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
          url_for("employee.reschedule_patient_appointment", locationid=locationid, _date=_date)
      ) 
  return render_template('reschedule/reschedule_patient.html', title=f"Reschedule", location_id=location.id, form=form,
      time_table=time_table,
      dates=table_dates,
      times=table_times,
      request_day=date,
      locations=locations,)

@employee.route('/employee/reschedule/patient/form/<int:patientid>/appointment/<int:appointmentid>/date/<string:date>/time/<string:time>/<int:aS_id>/<int:locationid>', methods=['GET', 'POST'])
@login_required
def reschedule_patient_form(patientid, appointmentid, date, locationid, aS_id, time):
  pass

@employee.route('/employee/reschedule/creations', methods=['POSTS'])
@login_required
def create_rescheduled_apt():
  flash("Appointment rescheduled!", 'success')
  return redirect(url_for("employee.e_home"))