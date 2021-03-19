from flask import Blueprint


main = Blueprint('main', __name__,
    static_folder='main/static/',
    template_folder='receita/views/'
)
