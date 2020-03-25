import pandas as pd
import datetime as dt
from ut import db
from ut.models import Location, AppointmentSlot, Employee

df = pd.read_csv('clinics.csv')
z = Employee(first='Zachary', last='Lopez', password='password', username='Zachary.Lopez@uth.tmc.edu', email="Zachary.Lopez@uth.tmc.edu")
for row in df.itertuples():
	l = Location(name=row.clinic, address=row.address)
	db.session.add(l)
	db.session.commit()
	print(f"{row.clinic} added to db!")

locations = Location.query.all()
#build days for AppointmentSlot
def build_days():
	days = []
	i=0
	start_date = dt.datetime.strptime("3/22/2020 8:00:00", "%m/%d/%Y %H:%M:%S")
	days.append(start_date)
	while i<31:
		start_date = start_date+dt.timedelta(days=1)
		days.append(start_date)
		i=i+1
	return days
days = build_days()
#build times for days for AppointmentSlot
def build_times(days):
	#times = []
	datetime_dct = {}
	for day in days:
		start_time = day
		times = []
		times.append(start_time)
		i=0
		while i < 36:
			start_time = start_time + dt.timedelta(minutes=15)
			times.append(start_time)
			i=i+1
		datetime_dct[day] = times		
	return datetime_dct
datetime_dct = build_times(days)

def create_appointmentslots(locations, days, datetime_dct):
	for location in locations:
		for day in days:
			for time in datetime_dct[day]:
				app = AppointmentSlot(location_id=location.id, date_time=time)
				db.session.add(app)
	db.session.commit()
	return f'IT IS DONE!'
example = create_appointmentslots(locations, days, datetime_dct)