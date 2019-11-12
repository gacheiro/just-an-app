from flask import Blueprint, request
from app.models import Usuario, Viagem
from app.api import UsuarioSchema, ViagemSchema

api_blueprint = Blueprint('api', __name__)

usuario_schema = UsuarioSchema()
viagem_schema = ViagemSchema()


@api_blueprint.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = Usuario.query.all()
        result = usuario_schema.dump(users, many=True)
        return {'users': result}
    else:
        return {}, 201
    

@api_blueprint.route('/users/<int:id>', methods=['GET', 'POST'])
def user(id):
    user = Usuario.query.get(id)
    return usuario_schema.dump(user)


@api_blueprint.route('/rides', methods=['GET', 'POST'])
def rides():
    if request.method == 'GET':
        rides = Viagem.query.all()
        result = viagem_schema.dump(rides, many=True)
        return {'rides': result}
    else:
        return {}, 201
