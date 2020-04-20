import flask
import os
from twilio.rest import Client
from ut.models import Location, Employee
from random import choice


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
    locations = Location.query.all()
    for location in locations:
        local_dict[location.id] = location.name
    return local_dict


def random_responder():
    "Right now will always return true, but in next database update will return employee phone call"
    employees = Employee.query.filter_by(is_active=True).all()
    if employees:
        lucky_employee = choice(employees)
        return lucky_employee
    return None
