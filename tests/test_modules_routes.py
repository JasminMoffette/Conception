import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_achat(client):
    response = client.get("/achat")
    assert response.status_code == 200

def test_reception(client):
    response = client.get("/reception")
    assert response.status_code == 200

def test_production(client):
    response = client.get("/production")
    assert response.status_code == 200

def test_ajustement(client):
    response = client.get("/ajustement")
    assert response.status_code == 200

def test_emplacement(client):
    response = client.get("/emplacement")
    assert response.status_code == 200
