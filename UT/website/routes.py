from flask import render_template, Blueprint, flash, redirect, url_for
from ut.models import Location, Appointment
from ut.website.forms import SignUp, CheckApt
from datetime import datetime
import numpy as np


website = Blueprint("website", __name__)


@website.route("/")
def home():
    locations = Location.query.all()
    return render_template("welcome.html", locations=locations)


@website.route("/<int:locationid>", methods=["GET", "POST"])
def samplelocation(locationid):
    appointments = Appointment.query.filter_by(location_id=locationid).all()
    location = Location.query.filter_by(id=locationid).first_or_404()
    appointments = []
    form = CheckApt()
    if form.validate_on_submit():
        flash("We submitted a form", "success")
        return redirect(
            url_for(
                "website.samplelocation_with_date",
                locationid=location.id,
                date=form.date.data,
            )
        )
    return render_template(
        "location.html",
        title="title",
        appointments=appointments,
        location=location,
        form=form,
        legend="Pick a date to check appointment availability",
    )


@website.route("/<int:locationid>/<string:date>", methods=["GET", "POST"])
def samplelocation_with_date(locationid, date):
    date = datetime.strptime(date, "%Y-%m-%d").replace(2020)
    appointments = Appointment.query.filter_by(schedule_date=date).all()
    location = Location.query.filter_by(id=locationid).first_or_404()
    dates = np.arange(date, date + 3, dtype="datetime64[D]")
    print(type(date))
    print(date)
    form = SignUp()
    if form.validate_on_submit():
        flash("Still got it!")
    return render_template(
        "appointment.html",
        title=f"{location.name} on {date} appointments",
        legend=f"{location.name} on {date} appointments. Submit Form to sign into an appointment.",
        form=form,
        appointments=appointments,
        dates=dates,
    )
