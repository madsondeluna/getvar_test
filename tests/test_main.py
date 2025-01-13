import pytest
from src.main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Uma ferramenta para consulta e anotação de arquivos VCF" in response.data

def test_consult_page(client):
    response = client.get('/consult')
    assert response.status_code == 200
    assert b"Insira o arquivo VCF" in response.data

def test_anotation_page(client):
    response = client.get('/anotation')
    assert response.status_code == 200
    assert b"Insira o arquivo VCF" in response.data
