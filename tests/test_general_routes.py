import pytest
from app import create_app

@pytest.fixture
def client():
    """Initialise une application Flask en mode test"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test de la page d'accueil"""
    response = client.get("/")
    assert response.status_code == 200

def test_plan(client):
    """Test de la page du plan"""
    response = client.get("/plan")
    assert response.status_code == 200

def test_afficher_entrepot(client):
    """Test de l'affichage d'un entrepôt"""
    response = client.get("/entrepot/entrepot1")
    assert response.status_code in [200, 404]  # 404 si l'entrepôt n'existe pas
