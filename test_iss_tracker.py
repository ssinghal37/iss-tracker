import pytest
from iss_tracker import app

@pytest.fixture
def client():
    #test client for Flask app
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_epochs(client):
    '''Testing /epochs'''
    response = client.get("/epochs")
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_epochs_limit(client):
    '''Testing /epochs?limit=x'''
    response = client.get("/epochs?limit=3")
    assert response.status_code == 200
    assert len(response.json) == 3

def test_get_epoch(client):
    '''Testing /epoch/<epoch>'''
    response = client.get("/epochs") # all epochs
    if response.json:
        ep = response.json[0]["EPOCH"] # one epoch to test
        ep_response = client.get(f'/epochs/{ep}')
        assert ep_response.status_code == 200
        assert ep_response.json["EPOCH"] == ep

def test_get_epoch_speed(client):
    '''Testing /epoch/<epoch>/speed'''
    response = client.get("/epochs")
    if response.json:
        ep = response.json[0]["EPOCH"] # epoch we test
        sp = client.get(f'/epochs/{ep}/speed')
        assert sp.status_code == 200
        assert "Instantaneous_Speed" in sp.json

def test_get_epoch_location(client):
    '''Testing /epoch/<epoch>/location'''
    response = client.get("/epochs")
    if response.json:
        ep = response.json[0]["EPOCH"] # epoch we test
        loc = client.get(f'/epochs/{ep}/location')
        assert loc.status_code == 200
        assert "Latitude" in loc.json
        assert "Longitude" in loc.json
        assert "Altitude" in loc.json
        assert "Geoposition" in loc.json

def test_now(client):
    '''Testing /now'''
    response = client.get("/now")
    assert response.status_code == 200
    assert "EPOCH" in response.json
    assert "Instantaneous_Speed" in response.json
    assert "Altitude" in response.json
    assert "Latitude" in response.json
    assert "Longitude" in response.json
    assert "Geoposition" in response.json


