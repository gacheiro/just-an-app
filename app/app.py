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

    @app.cli.command('create-db')
    def create_db():
        db.create_all()

    @app.cli.command('drop-db')
    def drop_db():
        if click.confirm('Are you sure?', abort=True):
            db.drop_all()

    return app
