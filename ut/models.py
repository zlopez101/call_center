from datetime import datetime
import enum
from ut import db, login_manager
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Status(enum.Enum):
    PENDING = "Pending"
    COMPLETE = "Complete"
    CONFIRMED = "Confirmed"
    CANCELLED = "Cancelled"
    NO_SHOW = "No show"


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
    referring_provider = db.Column(db.String())
    referral_id = db.Column(db.String())
    cancel_reason = db.Column(db.String(), default="")

    def complete_status(self):
        self.status = "COMPLETE"

    def cancel_appointment(self):
        self.status = "CANCELLED"

    def __repr__(self):
        return f"Appointment(patient {self.patient_scheduled} scheduled for {self.schedule_date_time}"


class Employee(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    first = db.Column(db.String())
    last = db.Column(db.String())
    is_active = db.Column(db.Boolean, default=False)
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
    confirmed = db.Column(db.Boolean, default=False)
    current_patient = db.Column(db.Boolean, default=False)
    appointment = db.relationship("Appointment", backref="patient", lazy=True)

    def confirm_patient_creation(self, expires_in=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_in)
        return s.dumps({"patient_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_patient(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            patient_id = s.loads(token)["patient_id"]
        except:
            return None
        return Patient.query.get(patient_id)

    def __repr__(self):
        return f"Patient({self.first} {self.last})"


class Location(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    address = db.Column(db.String())
    appointments = db.relationship("Appointment", backref="location", lazy=True)
    latitude = db.Column(db.String())
    longitude = db.Column(db.String())

    def __repr__(self):
        return f"Location({self.name})"
