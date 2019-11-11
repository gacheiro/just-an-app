from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_id = db.Column(db.String(80), 
        unique=True, nullable=False)
    nome = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), 
        unique=True, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
    viagens = db.relationship('Viagem', backref='usuario', lazy=True)


class Viagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    de = db.Column(db.String(100), nullable=False)
    para = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
