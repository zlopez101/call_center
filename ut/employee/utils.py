from ut.models import Location

def create_location_list():
  locations = Location.query.all()
  return locations

def create_location_dictionary():
  location_dict = {}
  locations = Location.query.all()
  for location in locations:
    location_dict[location.id] = location.name
  return location_dict
