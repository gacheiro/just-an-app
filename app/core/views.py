from flask import Blueprint, render_template
from app.models import Viagem

core_blueprint = Blueprint('core', __name__)


@core_blueprint.route('/caronas')
def caronas():
    viagens = Viagem.query.all()
    return render_template('core/caronas.html', rides=viagens)
