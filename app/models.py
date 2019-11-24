import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_id = db.Column(db.String(80), 
        unique=True, nullable=False)
    foto_url = db.Column(db.String(80), nullable=True)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), 
        unique=True, nullable=False)
    criado_em = db.Column(db.DateTime, 
        default=datetime.datetime.utcnow, nullable=False)
    viagens = db.relationship('Viagem', backref='usuario', lazy=True)


class Viagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'),
        nullable=False)
    de = db.Column(db.String(100), nullable=False)
    para = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    criado_em = db.Column(db.DateTime, 
        default=datetime.datetime.utcnow, nullable=False)


def create_user(claims):
    """Creates a user with firebase claims."""
    user = Usuario(
        nome=claims['name'],
        email=claims['email'],
        firebase_id=claims['sub'],
        foto_url=claims['picture'],
    )
    db.session.add(user)
    db.session.commit()
    return user
