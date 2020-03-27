from flask import Blueprint, redirect, url_for, flash, render_template
from ut.confirmations.view_helpers import send_confirm_text, parse_date_as_string
from ut.models import Patient, Location
from ut import db


confirmations = Blueprint("confirmations", __name__)


@confirmations.route(
    "/confirm_appointment/<int:locationid>/<int:patientid>/<string:date>/<string:_fom>"
)
def confirm_appointment(locationid, patientid, date, _fom):
    patient = Patient.query.filter_by(id=patientid).first()
    location = Location.query.filter_by(id=locationid).first()
    _day, _time = parse_date_as_string(date)
    token = patient.confirm_patient_creation()

    message_string = f"""
        This is the part where we would take the patient({patient.first} {patient.last}) stated phone number and use it to text them to confirm appointment at {location.name} on {_day} at {_time}. For now, let's keep texting Zach cause he doesn't mind! This is the link to confirm patient's appointment { url_for('.confirm_appointment_creation', token=token, _external=True)}
    """

    send_confirm_text("+17134306973", message_string)
    flash("Confirmation Text has been sent!", "success")
    if _fom == "public":
        return redirect(url_for("public.home"))
    else:
        return redirect(url_for("employee.e_home"))


@confirmations.route("/confirm_appointment_creation/<token>", methods=["GET", "POST"])
def confirm_appointment_creation(token):
    patient = Patient.verify_patient(token)
    if patient is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("public.home"))
    flash("Thanks for confirming your appointment!", "success")
    patient.confirmed = True
    db.session.commit()
    return redirect(url_for("public.home"))

