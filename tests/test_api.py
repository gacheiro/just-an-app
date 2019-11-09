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
    # disable auth while testing
    app.config['DISABLE_AUTH'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client


def test_get_users(client):
    response = client.get('/api/users')
    assert 200 == response.status_code
