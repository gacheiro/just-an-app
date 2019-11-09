from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


viagens = db.Table(
    'viagens',
    db.Column('usuario_id', db.Integer, 
        db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('viagem_id', db.Integer, 
        db.ForeignKey('viagem.id'), primary_key=True)
)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80),nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    criado_em = db.Column(db.DateTime, nullable=False)
    viagens = db.relationship('Viagem', secondary=viagens)


class Viagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    criado_por = db.Column(db.Integer, 
        db.ForeignKey('usuario.id'), nullable=False)
    de = db.Column(db.String(100), nullable=False)
    para = db.Column(db.String(100), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
