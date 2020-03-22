from UT import app
from UT.messenger import send_confirm_text
from UT.models import Location, AppointmentSlot
from UT.forms import SignUp
from flask import render_template, flash, request, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather

locations = Location.query.all()

@app.route('/')
def main():
	locations = Location.query.all()
	return render_template('welcome.html', locations=locations)


@app.route('/<int:locationid>')
def samplelocation(locationid):
	appointments = AppointmentSlot.query.filter_by(location_id=locationid).all()
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


@app.route("/voice", methods=['GET', 'POST'])
def voice():
	"""Respond to incoming phone calls with a 'Hello world' message"""
	# Start our TwiML response
	say = [f"For {location.name}, press {location.id}." for location in Location.query.all()]
	saying = ''.join(say)

	resp = VoiceResponse()
	gather = Gather(num_digits=1, action='/gather')
	gather.say(saying)
	resp.append(gather)
	return str(resp)


@app.route('/gather', methods=['GET', 'POST'])
def gather():
	resp = VoiceResponse()
	if 'Digits' in request.values:
		choice = request.values['Digits']
		for location in locations:
			if location.id == choice:
				resp.say(f'You Selected {location.name}.')
				resp.redirect(url_for('location', location_id=location.id))
	#resp.redirect('/voice')
	return str(resp)

@app.route('/location/<int:location_id>', methods=['GET', 'POST'])
def location(location_id):
	resp = VoiceResponse()
	here = Location.query.filter_by(id=location_id).first()
	resp.say(f'Welcome to the {here.name}. We are located at {here.addresss}. See you soon!')
	

