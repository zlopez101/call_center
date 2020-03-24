from flask import Blueprint, render_template
from ut.confirmations.view_helpers import twiml, send_confirm_text
from ut.models import Patient
from twilio.twiml.voice_response import VoiceResponse, Gather, 


confirmations = Blueprint(
    "confirmations", __name__, template_folder="confirm_templates"
)


@confirmations.route("/confirm_appointment/<int:patient_id>")
def confirm_appointment(patient_id):
    patient = Patient.query.filter_by(id=patient_id).first()
    message_string ="""
        This is the part where we would take the actual patient's stated
        phone number and use it to text them. For now, let's keep texting 
        Zach cause he doesn't mind!
    """

    return render_template("appt_confirm.html")
