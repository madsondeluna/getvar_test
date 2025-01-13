import pytest
from flask import Flask
from src.views import views

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(views)
    return app

@pytest.fixture
def client(app):
    return app.test_client()

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

def test_consult_post_no_file(client):
    response = client.post('/consult', data={})
    assert response.status_code == 200
    assert b"Escolha um arquivo VCF" in response.data

def test_anotation_post_no_file(client):
    response = client.post('/anotation', data={})
    assert response.status_code == 200
    assert b"Escolha um arquivo VCF" in response.data
