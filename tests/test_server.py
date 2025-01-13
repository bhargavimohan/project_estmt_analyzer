import pytest
from fastapi.testclient import TestClient
from src.server import app
import json

client = TestClient(app)


def test_receive_pdf_file():
    with open("pdfs/test_estmt.pdf", "rb") as file:
        response = client.post("/receive", files={"file": file})
    assert response.status_code in [200]
    assert response.json()["message"] in [
        "File received and analysis may have been completed"
    ]
    response = client.delete(
        "/delete/test_estmt.pdf"
    )  # delete the file after testing, test db not implementd
    # invalid file type
    with open("pdfs/test_estmt.txt", "rb") as file:
        response = client.post("/receive", files={"file": file})
    assert response.status_code == 422


def test_get_analyzed_pdfs_list():
    response = client.get("/analyzed-pdfs?year=1990")
    assert response.json()["message"] in ["No PDFs analyzed"]
    # response = client.get("/analyzed-pdfs")
    # assert response.status_code == 200
    # json_response = response.json()
    # assert "items" in json_response
    # assert isinstance(json_response["items"], list)


def test_get_analyzed_pdf():
    response = client.get("/analyzed/test_estmt.pdf")  # can change to unavailable.pdf
    if response.status_code == 200:
        output_json = json.loads(response.json())
        assert isinstance(output_json, dict)
    else:
        assert response.status_code == 404
        assert response.json() == {"message": "File not found"}


def test_delete_pdf_entry():
    response = client.delete("/delete/unavailable.pdf")  # can change to test_estmt.pdf
    if response.status_code == 200:
        assert response.json() == {
            "message": "File test_estmt.pdf deleted successfully"
        }
    else:
        assert response.status_code == 500
        assert response.json() == {
            "detail": "Failed to delete file: 404: File not found"
        }


def test_update_timestamp():
    response = client.patch(
        "/update-timestamp/test_estmt.pdf/2023.01.01"
    )  # can change to 2023-01-01
    if response.status_code == 200:
        assert response.json() == {
            "message": "Timestamp for file test_estmt.pdf updated successfully"
        }
    elif response.status_code == 404:
        assert response.json() == {"detail": "File not found"}
    elif response.status_code == 400:
        assert response.json() == {
            "detail": "Invalid timestamp format. Use 'YYYY-MM-DD'."
        }
    else:
        assert response.status_code == 500
