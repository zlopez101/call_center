from ut.models import Location

def create_location_list():
  locations = Location.query.all()
  return locations
