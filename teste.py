from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def teste_hello():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World!"}

def teste_quadrado():
    num = 4
    response = client.get(f"/quadrado/{num}")
    assert response.status_code == 200
    assert response.text == str(num ** 2)

def teste_scrapping():
    response = client.post(f"/webscrapping")
    assert response.status_code == 200
    assert response.json() == {"Dados":"inseridos com sucesso!"} or response.json() == {"Seção":"de navegação não encontrada."}

# no terminal, pytest teste.py