from fastapi.testclient import TestClient
from main import app
from .test_database import override_get_db  # activates test DB

client = TestClient(app)


def test_add_dataelement_dataset_not_found():
    response = client.post(
        "/add_dataelement",
        json={
            "name": "customer_id",
            "data_type": "string",
            "dataset_id": 999,
            "nullable":False
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Dataset not found"
