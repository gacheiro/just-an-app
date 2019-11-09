from flask import Blueprint, request
from app.api import UsuarioSchema, ViagemSchema

api_blueprint = Blueprint('api', __name__)

usuario_schema = UsuarioSchema()
viagem_schema = ViagemSchema()


usuarios = [
    {
        'id': 1,
        'nome': 'user 1',
        'email': 'user1@email.com',
    },
    {
        'id': 2,
        'nome': 'user 2',
        'email': 'user2@email.com',
    }
]


@api_blueprint.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = usuario_schema.dump(usuarios, many=True)
        return {'users': result}
    else:
        return {}
    

@api_blueprint.route('/users/<int:id>', methods=['GET', 'POST'])
def user(id):
    return usuario_schema.dump(dict(
        id=id,
        nome='Nome usuário',
        email='usuario@email.com',
        password='this should be filtered',
    ))
