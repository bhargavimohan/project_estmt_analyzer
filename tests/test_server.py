import pytest
from fastapi.testclient import TestClient
from src.server import app

client = TestClient(app)


def test_receive_pdf_file():
    with open("pdfs/test_estmt.pdf", "rb") as file:
        response = client.post("/receive", files={"file": file})
    assert response.status_code in [200]
    assert response.json()["message"] in ["Analysis completed"]

    # invalid file type
    with open("pdfs/test_estmt.txt", "rb") as file:
        response = client.post("/receive", files={"file": file})
    assert response.status_code == 422


def test_get_analyzed_pdfs_list():
    response = client.get("/analyzed-pdfs")
    assert response.status_code == 200
    json_response = response.json()
    assert "items" in json_response
    assert isinstance(json_response["items"], list)
