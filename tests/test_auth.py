import os
import pytest

import app.auth.views
from app import create_app


VALID_TOKEN = 'valid_token'
INVALID_TOKEN = 'invalid_token'


def verify_token(token, *args):
    if token == VALID_TOKEN:
        return {
            'sub': 'user_id',
        }
    else:
        return {}


@pytest.fixture
def client():
    os.environ['APP_SETTINGS'] = 'config.TestingConfig'
    os.environ['FLASK_ENV'] = 'test'
    # monkeypatch verify_token
    app.auth.views.verify_token = verify_token
    with create_app().test_client() as client:
        yield client


def test_auth__with_firebase_token(client):
    response = client.post('/auth', headers={
        'Authorization': 'Bearer ' + VALID_TOKEN
    })
    assert 200 == response.status_code


def test_auth__with_firebase_invalid_token(client):
    response = client.post('/auth', headers={
        'Authorization': 'Bearer ' + INVALID_TOKEN
    })
    assert 401 == response.status_code


def test_auth__without_token(client):
    response = client.post('/auth', headers={})
    assert 400 == response.status_code
