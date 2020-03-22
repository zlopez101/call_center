from flask import render_template, Blueprint, flash
from ut.models import Location, Appointment
from ut.website.forms import SignUp

website = Blueprint("website", __name__)


@website.route("/")
def home():
    locations = Location.query.all()
    return render_template("welcome.html", locations=locations)


@website.route("/<int:locationid>")
def samplelocation(locationid):
    appointments = Appointment.query.filter_by(location_id=locationid).all()
    location = Location.query.filter_by(id=locationid).first_or_404()
    appointments = []
    form = SignUp()
    if form.validate_on_submit():
        flash("We submitted a form", "success")
    return render_template(
        "location.html", title="title", appointments=appointments, location=location
    )
