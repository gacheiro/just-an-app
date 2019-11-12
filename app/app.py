import os
import click
from flask import Flask
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    from app.models import db
    db.init_app(app)
    migrate = Migrate(app, db)
    
    from app.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    from app.api import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # TODO: move cli commands out of create_app
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
        from app.models import Usuario

        fake = Faker()
        for _ in range(100):
            user = Usuario(
                nome=fake.name(),
                email=fake.email(),
                firebase_id=fake.uuid4()
            )
            db.session.add(user)
        db.session.commit()

    return app
