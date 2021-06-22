import os
from flask import Flask
from werkzeug.debug import DebuggedApplication
from werkzeug.utils import import_string

import exts
import blueprints as bp
from models.receitas import *
from models.usuario import *


def init_extensions(app):
    exts.db.init_app(app, dburi=app.config['SQLALCHEMY_DATABASE_URI'])


def init_db():
    exts.db.create_all()


def drop_db():
    exts.db.drop_all()


def create_app():
    app = Flask(__name__)

    # Settings
    if (fs := os.getenv('FLASK_SETTINGS')) and \
        (Config := import_string(fs, silent=True)):

        app.config.from_object(Config())

    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)
    app.config.from_pyfile('conf/application.conf.py')

    # Extensions
    init_extensions(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
        app.logger.warning(" * Debugger is active!")

        if app.wsgi_app.pin:
            app.logger.info(" * Debugger PIN: %s", app.wsgi_app.pin)

    # Blueprints
    # app.register_blueprint(bp.receita)
    # app.register_blueprint(bp.usuario)
    app.register_blueprint(bp.main)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', int(os.getenv('PORT', 5000)))
