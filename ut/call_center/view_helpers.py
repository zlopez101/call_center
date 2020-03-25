import flask
import os
from twilio.rest import Client
from ut.models import Location
from numpy import random

def get_creds():
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    _from_ = "+12057362289"
    return (TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, _from_)


def send_confirm_text(number, message):
    sid, token, _from_ = get_creds()
    client = Client(sid, token)
    message = client.messages.create(body=message, from_=_from_, to=number)
    return message


def twiml(resp):
    resp = flask.Response(str(resp))
    resp.headers["Content-Type"] = "text/xml"
    return resp

def _create_location_dict():
  local_dict = {}
  locations=Location.query.all()
  for location in locations:
    local_dict[location.id] = location.name
  return local_dict

def random_responder(logged_users):
  'Right now will always return true, but in next database update will return employee phone call'
  select_random = len(list(logged_users.keys()))
  random_index = random.choice(select_random, 1).tolist()
  return random_index
