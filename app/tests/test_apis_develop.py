from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from app.core import config
from app.main import app

client = TestClient(app)
# Local Config
# PORT="5000"
# SERVER="http://127.0.0.1"
# Dev Config
PORT = "80"
SERVER = "http://20.127.124.145"

URL = f"{SERVER}:{PORT}"


@pytest.fixture()
def api_token():
    # Get token.
    res = client.post(
        f"{URL}/token",
        headers={"Accept": "application/x-www-form-urlencoded"},
        data={"username": config.API_USERNAME, "password": config.API_PASSWORD,},
    )
    res_json = res.json()

    access_token = res_json["access_token"]
    token_type = res_json["token_type"]

    return f"{token_type} {access_token}"


def test_api_a(api_token):
    # Unauthorized request.
    response = client.get(f"{URL}/api_a/100")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    # Authorized but should raise 400 error.
    response = client.get(f"{URL}/api_a/a", headers={"Accept": "application/json", "Authorization": api_token,},)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Successful request.
    response = client.get(f"{URL}/api_a/200", headers={"Accept": "application/json", "Authorization": api_token,},)
    assert response.status_code == HTTPStatus.OK

    for val in response.json().values():
        assert isinstance(val, int)


def test_api_b(api_token):
    # Unauthorized request.
    response = client.get(f"{URL}/api_b/100")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    # Authorized but should raise 400 error.
    response = client.get(f"{URL}/api_b/b", headers={"Accept": "application/json", "Authorization": api_token,},)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    # Successful request.
    response = client.get(f"{URL}/api_b/0", headers={"Accept": "application/json", "Authorization": api_token,},)
    assert response.status_code == HTTPStatus.OK

    for val in response.json().values():
        assert isinstance(val, int)
