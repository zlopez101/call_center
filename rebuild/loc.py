import pandas as pd
from UT.models import Location
from UT import db

df = pd.read_csv('clinics.csv')

for row in df.itertuples():
	l = Location(name=row.clinic, address=row.address)
	db.session.add(l)
	db.session.commit()
	print(f"{row.clinic} added to db!")
