from fastapi.testclient import TestClient
from main import app

client=TestClient(app)

def test_add_dataset_success():
    response = client.post(
        "/add_dataset",
        json={
            "name": "sales_data",
            "description": "sales dataset"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "sales_data"
    assert "id" in data