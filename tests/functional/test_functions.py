import pytest
from ut.models import Employee


def test_home_page(create_client):
    response = create_client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Coronvirus Screening Website" in response.data


def test_locations_page(create_client):
    pass
