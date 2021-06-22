"""Arquivo para adicionar comandos a aplicacao"""

from flask.cli import AppGroup
from flask import current_app
import sys

sys.path.insert(0, '.') # Fix ImportError

import wsgi


db_cli = AppGroup('db')
app = wsgi.create_app()

app.cli.add_command(db_cli)


@db_cli.command('drop')
def db_drop():
    current_app.logger.info('Droping tables...')
    wsgi.drop_db()


@db_cli.command('init')
def db_init():
    current_app.logger.info('Creating tables...')
    wsgi.init_db()
