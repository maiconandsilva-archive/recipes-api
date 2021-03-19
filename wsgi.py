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


def create_app():
    app = Flask(__name__)

    # Settings
    cfg = import_string(os.getenv('FLASK_SETTINGS'), silent=True)
    if cfg:
        app.config.from_object(cfg())

    app.config.from_envvar('FLASK_SETTINGS_FILE', silent=True)
    app.config.from_pyfile('conf/application.conf.py')

    # Extensions
    init_extensions(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)

    # Blueprints
    # app.register_blueprint(bp.receita)
    # app.register_blueprint(bp.usuario)
    app.register_blueprint(bp.main)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', int(os.getenv('PORT', 5000)))
