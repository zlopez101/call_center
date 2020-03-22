from UT import db

class AppointmentSlot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	day = db.Column(db.DateTime, nullable=False)
	time = db.Column(db.Integer)
	slot_1 = db.Column(db.Boolean, default=False)
	slot_2 = db.Column(db.Boolean, default=False)
	location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
	
	def __repr__(self):
		return f"{self.day} @ {self.time}. First slope open: {self.slot_1}, Second slot open: {self.slot_2}"

class Location(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	address = db.Column(db.String)
	appointments = db.relationship(AppointmentSlot, backref='location', lazy=True)

	def __repr__(self):
		return f"{self.Name}"