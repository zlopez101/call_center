
from ut import db, bcrypt
from ut.models import Employee

z = Employee(first='Zachary', last='Lopez', password='password', username='Zachary.Lopez@uth.tmc.edu', email="Zachary.Lopez@uth.tmc.edu")
def create_employees():
    names = [
    "Lopez Zachary Zachary.Lopez@uth.tmc.edu",
    "Weinert Donna Donna.M.Weinert@uth.tmc.edu",
    "Vasquez Corina Corina.Arizpe@uth.tmc.edu",
    "Armstrong Madeline Madeline.C.Armstrong@uth.tmc.edu",
    "Mason Tamara Tamara.Mason@uth.tmc.edu",
    "Dorantes Izamar Izamar.Dorantes@uth.tmc.edu",
    "Curtain Johnna Johnna.L.Curtain@uth.tmc.edu",
    "Aguilar Karina Karina.Aguilar@uth.tmc.edu",
    "Williams Vanessa Vanessa.C.Williams@uth.tmc.edu",
    "Williams Monique Monique.Williams@uth.tmc.edu",
    "Keener Megan Megan.C.Keener@uth.tmc.edu",
    "Vassar Corina Corina.Strack@uth.tmc.edu",
    "Thomas Danisha Danisha.Thomas@uth.tmc.edu",
    "Flores Janine Janine.M.Flores@uth.tmc.edu",
    "Villatoro Mercedes Mercedes.Villatoro@uth.tmc.edu",
    'Center Call noemail', 
    'Site Web noemail'
    ]
    for name in names:
        lst = name.split(" ")
        add = Employee(first=lst[1], last=lst[0], email=lst[2], username=lst[2], password=bcrypt.generate_password_hash("password").decode("utf-8"))
        db.session.add(add)
        db.session.commit()




