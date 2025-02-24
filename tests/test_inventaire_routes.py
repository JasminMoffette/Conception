import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_inventaire_general(client):
    response = client.get("/inventaire/general")
    assert response.status_code == 200

def test_inventaire_libre(client):
    response = client.get("/inventaire/libre")
    assert response.status_code == 200

def test_inventaire_projet(client):
    response = client.get("/inventaire/projet")
    assert response.status_code == 200

def test_quincaillerie(client):
    response = client.get("/inventaire/quincaillerie")
    assert response.status_code == 200
