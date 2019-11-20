import os
import datetime
import pytest

from app import create_app
from app.models import db, Usuario, Viagem

users = [
    Usuario(
        nome='John Smith',
        email='johnsmith@example.com',
        firebase_id='1',
    ),
    Usuario(
        nome='Mary Smith',
        email='marysmith@example.com',
        firebase_id='2',
    ),
    Usuario(
        nome='Steve Smith',
        email='steve@example.com',
        firebase_id='3',
    ),
]

rides = [
    Viagem(
        usuario_id=1,
        de='Mossoró',
        para='Fortaleza',
        data=datetime.date.today() - datetime.timedelta(days=1), # yesterday
    ),
    Viagem(
        usuario_id=2,
        de='Assu',
        para='Mossoró',
        data=datetime.date.today() + datetime.timedelta(days=1), # tomorrow
    ),
    Viagem(
        usuario_id=3,
        de='Fortaleza',
        para='Mossoró',
        data=datetime.date.today(),
    ),
]


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


@pytest.fixture
def populate(client):
    db.session.add_all(users)
    db.session.add_all(caronas)
    db.session.commit()


def test_get_caronas(client, populate):
    rv = client.get('/caronas')
    assert b'John Smith' not in rv.data
    assert b'Mary Smith' in rv.data
    assert b'Steve Smith' in rv.data    
    assert rv.data.find(b'Steve Smith') < rv.data.find(b'Mary Smith') # output is sorted
    assert rv.data.count('Ofereço'.encode()) == 2
    assert rv.data.count('Mossoró'.encode()) == 2
    assert rv.data.count(b'Fortaleza') == 1
    assert rv.data.count(b'Assu') == 1
