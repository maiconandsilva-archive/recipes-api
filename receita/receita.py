from flask import Blueprint


receita = Blueprint(
    'receita',
    static_folder='receita/static/',
    template_folder='receita/templates/',
)