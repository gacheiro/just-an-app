import os
import tempfile
import pytest

from app import create_app
from app.models import db


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


def test_get_users(client):
    rv = client.get('/api/users')
    assert 200 == rv.status_code
    assert 'application/json', rv.headers.get('Content-Type')
    assert [] == rv.get_json().get('users')


def test_get_user(client):
    rv = client.get('api/users/1')
    assert 200 == rv.status_code


def test_new_user(client):
    rv = client.post('/api/users')
    assert 201 == rv.status_code


def test_get_rides(client):
    rv = client.get('/api/rides')
    assert 200 == rv.status_code


def test_get_ride(client):
    rv = client.get('/api/rides/1')
    assert 404 == rv.status_code


def test_new_ride(client):
    rv = client.post('api/rides')
    assert 201 == rv.status_code
