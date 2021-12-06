import base64
import io
import json

import pytest
from PIL import Image

from app import app


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get("/hello")
    assert b"region" in response.data


def test_ping(client):
    response = client.get("/ping")
    assert b"pong" in response.data


def test_dns_resolve(client):
    response = client.get("/dns/resolve?domain=example.com")
    assert response.status_code == 200


def test_images_fit_320(client):
    data = {}
    with open("tests/hello.png", "rb") as image_file:
        data["file"] = (image_file, "hello.png")
        response = client.post(
            "/images/fit/320",
            data=data,
            follow_redirects=True,
            content_type="multipart/form-data",
        )
        assert response.status_code == 200
        assert b"output" in response.data

        o = json.loads(response.data)

        im = Image.open(io.BytesIO(base64.b64decode(o["output"])))
        assert im.size == (320, 320)
