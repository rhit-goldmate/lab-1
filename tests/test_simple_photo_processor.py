import pytest

from app import create_app

@pytest.fixture
def app():
    app = create_app({'TESTING': True})
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_homepage_loads(client):
    homepage = client.get('/')
    assert b"Hello, World!" in homepage.data

def test_uploading_a_jpg_returns_a_jpg_image(client):
    assert False

def test_uploading_a_png_returns_an_jpg_image(client):
    assert False

def test_uploading_no_image_redirects_back_with_message(client):
    assert False

def test_non_images_are_not_allowed(client):
    assert False