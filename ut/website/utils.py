import datetime as dt



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

#build times for days for AppointmentSlot
def build_times():

	days = build_days()
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
