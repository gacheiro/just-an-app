import os
import pytest
from flask import request, session

import app.auth.routes
from app import create_app
from app.models import db

VALID_TOKEN = 'valid_token'
INVALID_TOKEN = 'invalid_token'
USER_ID = 'user_unique_id'


def verify_token(token, *args):
    if token == VALID_TOKEN:
        return {
            'sub': USER_ID,
        }
    else:
        return {}


# monkeypatch verify_token
app.auth.routes.verify_token = verify_token


@pytest.fixture
def client():
    os.environ['APP_SETTINGS'] = 'config.TestingConfig'
    os.environ['FLASK_ENV'] = 'test'
    app = create_app()
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()


def test_login_template(client):
    rv = client.get('/login')
    assert 200 == rv.status_code


def test_login_and_logout_flow(client):
    """Ensures user can login with a token and logout succesfully."""
    rv = client.post('/login', headers={
        'Authorization': 'Bearer ' + VALID_TOKEN
    }, follow_redirects=True)
    assert 200 == rv.status_code
    # ensures session cookies are set on login
    assert 'user_id' in session
    assert USER_ID == session['user_id']
    # ensures session cookies are removed on logout
    rv = client.post('/logout', follow_redirects=True)
    assert 200 == rv.status_code
    assert 'user_id' not in session


def test_login__with_invalid_token(client):
    rv = client.post('/login', headers={
        'Authorization': 'Bearer ' + INVALID_TOKEN
    })
    assert 401 == rv.status_code
    assert 'user_id' not in session


def test_login__without_token(client):
    rv = client.post('/login', headers={})
    assert 400 == rv.status_code
    assert 'user_id' not in session
