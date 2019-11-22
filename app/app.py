import os
import click
from flask import Flask
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config['FIREBASE_API_KEY'] = os.environ['FIREBASE_API_KEY']

    from app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)

    from app.core import core_blueprint
    app.register_blueprint(core_blueprint)
    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    register_commands(app, db)
    register_template_filters(app)
    return app


def register_commands(app, db):
    
    # TODO: move cli commands to db/models.py
    @app.cli.command('create-db')
    def create_db():
        db.create_all()

    @app.cli.command('drop-db')
    def drop_db():
        if click.confirm('Are you sure?', abort=True):
            db.drop_all()

    @app.cli.command('populate-db')
    def populate_db():
        from faker import Faker
        from app.models import Usuario, Viagem

        fake = Faker('pt_BR')
        for _ in range(100):
            user = Usuario(
                nome=fake.name(),
                email=fake.email(),
                firebase_id=fake.uuid4()
            )
            db.session.add(user)
        db.session.commit()
        # add rides for the 20 fst users
        for user_id in range(1, 21):
            ride = Viagem(
                usuario_id=user_id,
                de=fake.city(),
                para=fake.city(),
                data=fake.date_time_between(start_date="-20d", end_date="+20d"),
            )
            db.session.add(ride)
        db.session.commit()


def register_template_filters(app):
    from app.util.filters import weekday, datetimeformat
    app.template_filter('weekday')(weekday)
    app.template_filter('datetimeformat')(datetimeformat)
