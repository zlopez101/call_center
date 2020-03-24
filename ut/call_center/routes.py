from flask import render_template, Blueprint, url_for, flash, request
from ut.models import Location, Appointment
from ut.call_center.view_helpers import twiml, send_confirm_text
from twilio.twiml.voice_response import VoiceResponse, Gather

call_center = Blueprint("call_center", __name__)


@call_center.route("/confirm_app")
def confirm():
    text = send_confirm_text("+17134306973", "message")
    return f"hello confirm {text}"


@call_center.route("/welcome_to_call_center", methods=["GET", "POST"])
def welcome():
    response = VoiceResponse()
    response.say("hello", voice="alice", language="en-GB")
    response.redirect(url_for("call_center.voice"))
    return twiml(response)


@call_center.route("/voice", methods=["GET", "POST"])
def voice():
    """Respond to incoming phone calls with a 'Hello world' message"""
    # Start our TwiML response
    locations = Location.query.all()
    location_dict = {}
    for location in locations:
        location_dict[location.id] = location.name
    say = [f"For {location.name}, press {location.id} " for location in locations]

    resp = VoiceResponse()
    gather = Gather(num_digits=2, action=url_for("call_center.gather"))
    for i in say:
        gather.say(i)
        gather.pause(1)
    resp.append(gather)
    return str(resp)


@call_center.route("/gather", methods=["GET", "POST"])
def gather():
    locations = Location.query.all()
    location_dict = {}
    for location in locations:
        location_dict[location.id] = location.name
    resp = VoiceResponse()
    choice = int(request.form["Digits"])

    if choice in location_dict:
        resp.say(f"You selected {location_dict[choice]}")
        resp.redirect(url_for("call_center.call_location", location_id=choice))
        return twiml(resp)

    return _redirect_welcome()


@call_center.route("/location/<int:location_id>", methods=["GET", "POST"])
def call_location(location_id):
    resp = VoiceResponse()
    here = Location.query.filter_by(id=location_id).first()
    resp.say(
        f"Welcome to the {here.name}. We are located at {here.address}. See you soon!"
    )

    return twiml(resp)


def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for("call_center.welcome"))

    return twiml(response)
