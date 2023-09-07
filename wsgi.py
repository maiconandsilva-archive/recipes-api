import os
import pprint as pp
import wtforms_json
from flask import Flask
from werkzeug.debug import DebuggedApplication
from werkzeug.utils import import_string

import exts
import blueprints as bp
from models.receitas import *
from models.usuario import *


def init_extensions(app):
    exts.db.init_app(app, dburi=app.config['SQLALCHEMY_DATABASE_URI'])
    exts.csrf.init_app(app)
    wtforms_json.init()


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

    # UPGRADE VERSION WHEN THE NEWER API IS NOT COMPATIBLE WITH THE PREVIOUS
    app.config.setdefault('API_VERSION', '1')

    # Extensions
    init_extensions(app)

    if app.debug:
        app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
        app.logger.debug(" * Debugger is active!")

        if app.wsgi_app.pin:
            app.logger.debug(" * Debugger PIN: %s", app.wsgi_app.pin)

    # Blueprints
    # URL API
    bp.bp_api.url_prefix = '/api/v{API_VERSION}'.format(**app.config)

    # Static folder of main is the same as the app
    bp.bp_main.static_folder = app.static_folder

    app.register_blueprint(bp.bp_api)
    app.register_blueprint(bp.bp_main)
    app.register_blueprint(bp.bp_errors)

    def get_bp_urls(blueprint):
        from flask import Flask
        temp_app = Flask(__name__)
        temp_app.register_blueprint(blueprint)
        return [rule for rule in temp_app.url_map.iter_rules()]

    print([(f.__annotations__, f.__doc__) for f in app.view_functions.values()])

    # rules = get_bp_urls(bp.bp_api)

    # for rule in rules:
    #     if rule.endpoint != 'static':
    #         print(rule.methods)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run('0.0.0.0', int(os.getenv('PORT', 5000)))
