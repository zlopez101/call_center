"""
from ut import db
from ut.models import Employee

names = [
    #'Zachary Lopez',
    "Donna Weinert",
    "Corina Vasquez",
    "Madeline Armstrong",
    "Tamara _blank_",
    "Izamar _blank_",
    "Johnna Curtain",
    "Karina Aguilar",
    "Vanessa _blank_",
    "Monique Williams",
    "Megan Keener",
    "Corina Strack",
    "Danisha Thomas",
    "Marby _blank_",
    "Mercedes Villatoro",
    'Call Center'
    'Web Site'
]

for name in names:
    lst = name.split(" ")
    add = Employee(first=lst[0], last=lst[-1])
    db.session.add(add)
    db.session.commit()
    print(f"{lst[0]} {lst[-1]} added")
"""

