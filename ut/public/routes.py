from flask import render_template, Blueprint, flash, redirect, url_for, current_app
from ut.models import Location, Appointment, Patient, Employee, AppointmentSlot
from ut.public.forms import SignUp, CheckApt
from ut.public.utils import create_times, create_table_dict, parse_date_as_string
from ut import db
import datetime
import numpy as np


public = Blueprint("public", __name__, template_folder="public_pages")


@public.route("/")
def home():
    locations = Location.query.all()
    return render_template("welcome.html", locations=locations)


@public.route("/about")
def about():
    locations = Location.query.all()
    return render_template("about.html", locations=locations)


@public.route("/insurance_and_COVID19")
def insurance():
    locations = Location.query.all()
    return render_template("insurance.html", locations=locations)


@public.route("/<int:locationid>", methods=["GET", "POST"])
def samplelocation(locationid):
    locations = Location.query.all()
    appointments_at_location = Appointment.query.filter_by(location_id=locationid).all()
    location = Location.query.filter_by(id=locationid).first_or_404()
    key = current_app.config["MAP_KEY"]
    google = (
        "https://maps.googleapis.com/maps/api/staticmap?center="
        + location.address
        + "&zoom=14&markers="
        + location.address
        + "&size=400x400&key="
        + key
    )
    form = CheckApt()
    if form.validate_on_submit():
        flash(
            f"{location.name} schedule for next five days after your chosen date {form.date.data.strftime('%m/%d')}",
            "success",
        )
        date = form.date.data
        date = date.replace(2020)
        date_and_time = datetime.datetime.combine(
            date, datetime.time(hour=8, minute=0, second=0)
        )
        return redirect(
            url_for(
                "public.samplelocation_with_date",
                locationid=location.id,
                date=date_and_time,
            )
        )
    return render_template(
        "location.html",
        title="title",
        appointments=appointments_at_location,
        location=location,
        form=form,
        legend="Pick a date to check appointment availability",
        google=google,
        locations=locations,
    )


@public.route("/<int:locationid>/<string:date>", methods=["GET", "POST"])
def samplelocation_with_date(locationid, date):
    locations = Location.query.all()
    _date, _ = parse_date_as_string(date)

    date = datetime.datetime.strptime(_date, "%Y-%m-%d")

    appointmentslots = AppointmentSlot.query.filter(
        AppointmentSlot.date_time >= date,
        AppointmentSlot.location_id == locationid,
        AppointmentSlot.date_time < date + datetime.timedelta(days=5),
    ).all()

    location = Location.query.filter_by(id=locationid).first_or_404()

    table_dates = np.arange(
        date, date + datetime.timedelta(days=5), dtype="datetime64[D]"
    )
    table_times = create_times()
    time_table = create_table_dict(appointmentslots, table_times, table_dates)

    # for table configuration
    table_dates = [
        datetime.datetime.strptime(date, "%Y-%m-%d")
        for date in np.datetime_as_string(table_dates)
    ]

    return render_template(
        "appointment.html",
        title=f"{location.name} on {date} appointments",
        legend=f"{location.name} on {date} appointments. Submit Form to sign into an appointment.",
        location_id=location.id,
        time_table=time_table,
        dates=table_dates,
        times=table_times,
        request_day=date,
        locations=locations,
    )


@public.route(
    "/my_appointment/<int:locationid>/<string:date>/<string:request_time>/<int:aS_id>",
    methods=["GET", "POST"],
)
def my_appointment(locationid, date, request_time, aS_id):
    locations = Location.query.all()
    aS = AppointmentSlot.query.filter_by(id=aS_id).first()
    location = Location.query.filter_by(id=locationid).first()
    request_date_as_datetime = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    google = (
        "https://maps.googleapis.com/maps/api/staticmap?center="
        + location.address
        + "&zoom=14&markers="
        + location.address
        + "&size=400x400&key="
        + current_app.config["MAP_KEY"]
    )
    _day, _time = parse_date_as_string(date)
    form = SignUp()
    if form.validate_on_submit():
        "Creating the new patient"
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

        "Creating the new Appointment"
        web_employee = Employee.query.filter_by(first="Web").first()
        new_appointment = Appointment(
            created_by=web_employee.id,
            date_created=datetime.datetime.utcnow(),
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
                _fom="public",
            )
        )
    return render_template(
        "my_appointment.html",
        title="Sign up Today",
        legend=f"Sign Up for an Appointment on {_day} at {_time} at {location.name}.",
        form=form,
        locations=locations,
        location=location,
        google=google,
    )
