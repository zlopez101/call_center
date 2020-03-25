from ut import logged_on_employees_call_center_dict


def add_user(userid):
  c = list(logged_on_employees_call_center_dict.values())
  ld = {}
  c.append(userid)
  for i, value in enumerate(c):
    ld[i] = value
  return ld

def remove_user(userid):
  c = list(logged_on_employees_call_center_dict.values())
  ld = {}
  c.remove(userid)
  for i, value in enumerate(c):
    ld[i, value]
  return ld

