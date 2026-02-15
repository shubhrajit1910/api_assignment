from fastapi.testclient import TestClient
from main import app
from .test_database import override_get_db

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


def test_add_dataset_duplicate_name():
    # First insert
    client.post(
        "/add_dataset",
        json={
            "name": "sales_data",
            "description": "sales dataset"
        }
    )

    # Duplicate insert
    response = client.post(
        "/add_dataset",
        json={
            "name": "sales_data",
            "description": "another dataset"
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Dataset name must be unique"