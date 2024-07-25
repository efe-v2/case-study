from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_recommend():
    user_id = "00172f1d9a71e9a8de0aa34288a6b19b"
    response = client.get(f"/recommend?user_id={user_id}")
    assert response.status_code == 200
    json_response = response.json()
    assert "recommendations" in json_response
    assert isinstance(json_response["recommendations"], list)
