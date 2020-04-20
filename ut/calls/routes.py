from flask import Blueprint, url_for, request, current_app
from ut.models import Location, Employee
from ut.calls.view_helpers import (
    twiml,
    send_confirm_text,
    _create_location_dict,
    random_responder,
)
from twilio.twiml.voice_response import VoiceResponse, Gather


calls = Blueprint("calls", __name__)


@calls.route("/confirm_app")
def confirm():
    text = send_confirm_text("+17134306973", "message")
    return f"hello confirm {text}"


@calls.route("/welcome_to_call_center", methods=["GET", "POST"])
def welcome():
    response = VoiceResponse()
    response.say("Welcome to the U T Physicians Corona Virus Testing Call Line.")
    response.pause(1)
    response.say(
        "Listen for the Clinic you wish to schedule a screening at and press the corresponding key on your keypad"
    )
    response.redirect(url_for("call_center.voice"))
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
    gather = Gather(num_digits=2, action=url_for("call_center.gather"))
    for i in say:
        gather.say(i)
        gather.pause(1)
    resp.append(gather)
    return str(resp)


@calls.route("/gather", methods=["GET", "POST"])
def gather():
    resp = VoiceResponse()
    location_dict = _create_location_dict()
    choice = int(request.form["Digits"])
    if choice in location_dict:
        resp.say(f"You selected {location_dict[choice]}")
        resp.redirect(url_for("call_center._call_location", location_id=choice))
        return twiml(resp)

    return _redirect_welcome()


@calls.route("/call_center/<int:location_id>", methods=["GET", "POST"])
def _call_location(location_id):
    employee = random_responder()
    resp = VoiceResponse()
    responder = Employee.query.filter_by(id=employee.id).first()
    print(responder.first, responder.last)
    here = Location.query.filter_by(id=location_id).first()
    resp.say(f"Welcome to the {here.name} clinic")
    resp.pause(1)
    resp.say(f"{responder.first} {responder.last} will help you now. Thanks")
    resp.pause(1)
    resp.say(f"We are located at {here.address}. See you soon!")

    return twiml(resp)


def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for("call_center.welcome"))

    return twiml(response)
