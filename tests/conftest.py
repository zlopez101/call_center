import os
import tempfile

import pytest

import ut.models as models
from ut import create_app, db
from ut.config import Config_Tester
from ut.rebuild.employee import create_employees
from ut.rebuild.loc import build_appointment_slots, create_locations


@pytest.fixture(scope="module")
def new_employee():
    employee = models.Employee(
        first="test",
        last="employee",
        username="test_employee@yahoo.com",
        email="test_employee@yahoo.com",
        password="password",
    )
    # db.session.add(employee)
    # db.session.commit()
    return employee


@pytest.fixture(scope="session")
def create_client():
    app = create_app(config_class=Config_Tester)
    with app.app_context():
        db.create_all()

        # Have to create database structure so the test client knows how to navigate everywhere
        create_employees()
        create_locations(r"C:\Users\zachl\Codes\call_center\ut\rebuild\clinics.csv")
        build_appointment_slots()

        # this is where the testing happens
        yield app.test_client()

        # destroy database
        db.drop_all()
