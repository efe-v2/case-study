from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_user_interaction():
    interaction_data = {
        "date": "2024-07-25T12:34:56Z",
        "user_id": "test",
        "session_id": "test",
        "page_type": "productDetail",
        "item_id": "test",
        "category": ["test"],
        "product_price": 299.99,
        "old_product_price": 349.99
    }
    response = client.post("/user-interaction", json=interaction_data)
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["status"] == "Message sent"
    assert "message_id" in json_response
