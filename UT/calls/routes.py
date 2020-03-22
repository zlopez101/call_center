from flask import render_template, Blueprint, url_for, flash, request
from ut.models import Location, Appointment
from ut.calls.view_helpers import twiml
from ut.calls.messenger import send_confirm_text
from twilio.twiml.voice_response import VoiceResponse, Gather

calls = Blueprint("calls", __name__)


@calls.route("/confirm_app")
def confirm():
    text = send_confirm_text("+17134306973", "message")
    return f"hello confirm {text}"


@calls.route("/welcome_to_call_center", methods=["GET", "POST"])
def welcome():
    response = VoiceResponse()
    response.say("hello", voice="alice", language="en-GB")
    response.redirect(url_for("calls.voice"))
    return twiml(response)


@calls.route("/voice", methods=["GET", "POST"])
def voice():
    """Respond to incoming phone calls with a 'Hello world' message"""
    # Start our TwiML response
    locations = Location.query.all()
    location_dict = {}
    for location in locations:
        location_dict[location.id] = location.name
    say = [f"For {location.name}, press {location.id} " for location in locations]

    resp = VoiceResponse()
    gather = Gather(num_digits=2, action=url_for("calls.gather"))
    for i in say:
        gather.say(i)
        gather.pause(1)
    resp.append(gather)
    return str(resp)


@calls.route("/gather", methods=["GET", "POST"])
def gather():
    locations = Location.query.all()
    location_dict = {}
    for location in locations:
        location_dict[location.id] = location.name
    resp = VoiceResponse()
    choice = int(request.form["Digits"])

    if choice in location_dict:
        resp.say(f"You selected {location_dict[choice]}")
        resp.redirect(url_for("calls.call_location", location_id=choice))
        return twiml(resp)

    return _redirect_welcome()


@calls.route("/location/<int:location_id>", methods=["GET", "POST"])
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
    response.redirect(url_for("calls.welcome"))

    return twiml(response)
