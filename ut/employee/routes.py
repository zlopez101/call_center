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
    LoginForm_db_not_formed,
    SelectApt,
    PatientData,
)
from ut.employee.utils import create_location_list
from flask_login import current_user, login_required, login_user, logout_user
from ut.models import Employee, Location, AppointmentSlot, Patient, Appointment
from ut.public.forms import SignUp, CheckApt
from ut.public.utils import parse_date_as_string, create_times, create_table_dict
from ut import db
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
        "e_home.html",
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
    ).all()
    patients = (
        Patient.query.join(Appointment)
        .filter(
            Appointment.location_id == loc.id,
            Appointment.schedule_date_time > beginning_of_date,
            Appointment.schedule_date_time < end_of_date,
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
    "/employee/patient_inquiry/<int:patientid>/<int:locationid>/<string:_date>",
    methods=["GET", "POST"],
)
@login_required
def patient_inquiry(patientid, locationid, _date):
    locations = create_location_list()
    patient = Patient.query.filter_by(id=patientid).first()
    appointment = Appointment.query.filter_by(patient_scheduled=patient.id).first()
    form = PatientData()
    form.appointment_location.choices = [
        (location.id, location.name) for location in locations
    ]
    if form.validate_on_submit():
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
    form.confirmed.data = patient.confirmed
    form.referring_provider.data = patient.referring_provider
    form.referral_number.data = patient.referral_id
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
        form=form,
        legend=f"{patient.first} {patient.last}",
        side_form=side_form,
        side_legend="Choose a different appointment table.",
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
    form = LoginForm_db_not_formed()
    if form.validate_on_submit():

        employee = Employee.query.filter_by(last=form.last.data).first()
        if employee:
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
    return render_template("login.html", title="Login", form=form, legend="Login")


@employee.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_emp = Employee(first=form.first.data, last=form.last.data)
        db.session.add(new_emp)
        db.session.commit()
        flash("you registered!", "success")
        return redirect(url_for("employee.login"))
    return render_template(
        "register.html", title="Registration Page", form=form, legend="Register"
    )


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
    return render_template("e_about.html")
