import datetime as dt
import os
from ut.models import Location
from flask import current_app

# create map url
def maps(location):
    link = "https://www.google.com/maps/place/" + location.address
    google = (
        "https://maps.googleapis.com/maps/api/staticmap?center="
        + location.address
        + "&zoom=13&markers="
        + location.address
        + "&size=300x300&key="
        + current_app.config["MAP_KEY"]
    )
    return link, google


# build days for AppointmentSlot
def build_days():
    days = []
    i = 0
    start_date = dt.datetime.strptime("3/22/2020 8:00:00", "%m/%d/%Y %H:%M:%S")
    days.append(start_date)
    while i < 31:
        start_date = start_date + dt.timedelta(days=1)
        days.append(start_date)
        i = i + 1
    return days


# build times for days for AppointmentSlot
def build_times():

    days = build_days()
    # times = []
    datetime_dct = {}
    for day in days:
        start_time = day
        times = []
        times.append(start_time)
        i = 0
        while i < 36:
            start_time = start_time + dt.timedelta(minutes=15)
            times.append(start_time)
            i = i + 1
        datetime_dct[day] = times
    return datetime_dct


# create times for AppointmentSlot
def create_times():
    time_start = dt.datetime.strptime("08:00:00", "%H:%M:%S")
    times = []
    times.append(time_start)
    i = 0
    while i < 36:
        time_start = time_start + dt.timedelta(minutes=15)
        times.append(time_start)
        i = i + 1
    return times


# create dictionary with times as keys for table data
def create_table_dict(appointmentslots, table_times, table_dates):
    time_table = {}
    # match appointment to their time and date
    for time in table_times:
        time_table[time] = []
        for date in table_dates:
            "need to the appointment"
            time_table[time].append(
                [
                    aS
                    for aS in appointmentslots
                    if aS.date_time.strftime("%Y-%m-%d %H:%M").split(" ")[-1]
                    == time.strftime("%H:%M")
                    and aS.date_time.strftime("%Y-%m-%d %H:%M").split(" ")[0]
                    == date.astype(object).strftime("%Y-%m-%d")
                ]
            )
    return time_table


# work with datetime as string -> date as string, time as string
def parse_date_as_string(_date_as_string):
    "This function returns two strings, 1 is the date and 1 is the time"
    _day = _date_as_string.split(" ")[0]
    _time = _date_as_string.split(" ")[-1]
    return _day, _time
