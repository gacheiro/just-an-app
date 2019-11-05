from flask import Blueprint
from app.api import UsuarioSchema, ViagemSchema

api_blueprint = Blueprint('api', __name__)

usuario_schema = UsuarioSchema()
viagem_schema = ViagemSchema()


@api_blueprint.route('/users', methods=['GET'])
def get_users():
    return 'list of users'


@api_blueprint.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return usuario_schema.dump(dict(
        id=id,
        nome='Nome usuário',
        email='usuario@email.com',
        password='this should be filtered',
    ))
