import pytest
from ut.models import Employee


def test_home_page(create_client):
    response = create_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Coronvirus Screening Website" in response.data


def test_locations_page(create_client):
    response = create_client.get("/1")
    assert response.status_code == 200
    assert b"11452 Space Center Blvd Houston, Tx 77059" in response.data
    assert b"Pick a date to check appointment availability" in response.data
