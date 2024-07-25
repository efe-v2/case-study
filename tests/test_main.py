from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_read_redoc():
    response = client.get("/redoc")
    assert response.status_code == 200

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "I am standing..."}