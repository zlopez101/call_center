from datetime import datetime
import enum
from ut import db, login_manager
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Status(enum.Enum):
    PENDING = "Pending"
    COMPLETE = "Complete"
    NO_SHOW = "No show"
    CANCELLED = "Cancelled"

class AppointmentSlot(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
	date_time = db.Column(db.DateTime)
	slot_1 = db.Column(db.Boolean, default=False)
	slot_1_appointment = db.Column(db.Integer, db.ForeignKey("appointment.id"))

	def __repr__(self):
		return f'{self.id} at {self.location_id} on {datetime.strftime(self.date_time, "%m/%d %H:%M")}'




class Appointment(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("employee.id"))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    patient_scheduled = db.Column(db.Integer, db.ForeignKey("patient.id"))
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"))
    schedule_date_time = db.Column(db.DateTime)
    status = db.Column(db.Enum(Status))
    cancel_reason = db.Column(db.String(), default="")

    def __repr__(self):
        return f"Appointment(patient {self.patient_scheduled} scheduled for {self.schedule_date_time}"


class Employee(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    last = db.Column(db.String())
    scheduled = db.relationship("Appointment", backref="scheduler", lazy=True)

    def __repr__(self):
        return f"Employee({self.first} {self.last})"


class Patient(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    first = db.Column(db.String())
    last = db.Column(db.String())
    dob = db.Column(db.Date)
    phone = db.Column(db.String())
    email = db.Column(db.String())
    lang = db.Column(db.String())
    ins = db.Column(db.String())
    appointment = db.relationship("Appointment", backref="patient", lazy=True)

    def __repr__(self):
        return f"Patient({self.first} {self.last})"


class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    appointments = db.relationship("Appointment", backref="location", lazy=True)

    def __repr__(self):
        return f"Location({self.name})"
