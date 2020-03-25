from flask import Blueprint, url_for, request
from ut.models import Location, Employee
from ut.call_center.view_helpers import twiml, send_confirm_text, _create_location_dict, random_responder
from twilio.twiml.voice_response import VoiceResponse, Gather
from ut import logged_on_employees_call_center_dict

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
    resp = VoiceResponse()
    location_dict = _create_location_dict()
    choice = int(request.form["Digits"])

    if choice in location_dict:
      resp.say(f"You selected {location_dict[choice]}")
      resp.redirect(url_for('call_center._call_location',location_id=choice))
      return twiml(resp)

    return _redirect_welcome()


@call_center.route("/call_center/<int:location_id>", methods=["GET", "POST"])
def _call_location(location_id):
  index = random_responder(logged_on_employees_call_center_dict)
  resp = VoiceResponse()
  responder = Employee.query.get(index[0])
  print(responder.first, responder.last)
  here = Location.query.filter_by(id=location_id).first()
  resp.say(
      f"Welcome to the {here.name}")
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
