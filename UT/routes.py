
from UT import app
from UT.messenger import send_confirm_text
from UT.models import Location, Appointment
from UT.forms import SignUp
from UT.view_helpers import twiml
from flask import render_template, flash, request, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather

locations = Location.query.all()
location_dict = {}
for location in locations:
	location_dict[location.id] = location.name

@app.route('/')
def main():
	locations = Location.query.all()
	return render_template('welcome.html', locations=locations)


@app.route('/<int:locationid>')
def samplelocation(locationid):
	appointments = Appointment.query.filter_by(location_id=locationid).all()
	location=Location.query.filter_by(id=locationid).first_or_404()
	appointments = []
	form = SignUp()
	if form.validate_on_submit():
		flash('We submitted a form', 'success')
	return render_template('location.html', title='title', appointments=appointments, location=location)



@app.route('/confirm_app')
def confirm():
	text = send_confirm_text("+17134306973")
	return f"hello confirm {text}"

@app.route('/welcome_to_call_center',  methods=['GET', 'POST'])
def welcome():
	response = VoiceResponse()
	response.say("hello",	voice="alice", language="en-GB")
	response.redirect(url_for('voice'))
	return twiml(response) 


@app.route("/voice", methods=['GET', 'POST'])
def voice():
	"""Respond to incoming phone calls with a 'Hello world' message"""
	# Start our TwiML response
	say = [f"For {location.name}, press {location.id} " for location in locations]

	resp = VoiceResponse()
	gather = Gather(num_digits=2, action=url_for('gather'))
	for i in say:
		gather.say(i)
		gather.pause(1)
	resp.append(gather)
	return str(resp)

@app.route('/gather', methods=['GET', 'POST'])
def gather():
	resp = VoiceResponse()
	choice = int(request.form['Digits'])
	
	if choice in location_dict:
		resp.say(f"You selected {location_dict[choice]}")
		resp.redirect(url_for('location', location_id=choice))
		return twiml(resp)

	return _redirect_welcome()



@app.route('/location/<int:location_id>', methods=['GET', 'POST'])
def location(location_id):
	resp = VoiceResponse()
	here = Location.query.filter_by(id=location_id).first()
	resp.say(f'Welcome to the {here.name}. We are located at {here.address}. See you soon!')
	
	return twiml(resp)

def _redirect_welcome():
    response = VoiceResponse()
    response.say("Returning to the main menu", voice="alice", language="en-GB")
    response.redirect(url_for('welcome'))

    return twiml(response)
