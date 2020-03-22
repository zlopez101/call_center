from models import Location

say = [f"for{location.name}, press {location.id}" for location in Location.query.all()]
print(say)