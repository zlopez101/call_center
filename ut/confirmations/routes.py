from flask import Blueprint, render_template

confirmations = Blueprint(
    "confirmations", __name__, template_folder="confirm_templates"
)


@confirmations.route("/confirm_appointment/<int:patient_id>")
def confirm_appointment():
    return render_template("appt_confirm.html")
