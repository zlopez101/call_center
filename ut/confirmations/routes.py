from flask import Blueprint, redirect, url_for, flash
from ut.confirmations.view_helpers import send_confirm_text, parse_date_as_string
from ut.models import Patient, Location



confirmations = Blueprint(
    "confirmations", __name__
)


@confirmations.route(
    "/confirm_appointment/<int:locationid>/<int:patientid>/<string:date>"
)
def confirm_appointment(locationid, patientid, date):
    patient = Patient.query.filter_by(id=patientid).first()
    location = Location.query.filter_by(id=locationid).first()
    _day, _time = parse_date_as_string(date)

    message_string = f"""
        This is the part where we would take the patient({patient.first} {patient.last}) stated phone number and use it to text them to confirm appointment at {location.name} on {_day} at {_time}. For now, let's keep texting Zach cause he doesn't mind!
    """

    send_confirm_text("+17134306973", message_string)
    flash("Confirmation Text has been sent!", "success")
    return redirect(url_for("public.home"))
    
