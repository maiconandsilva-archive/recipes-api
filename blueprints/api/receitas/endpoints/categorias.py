from flask.json import jsonify

from models.receitas import Categoria
from models.serialization import serialize
from ..blueprint import categorias


@categorias.route('/')
def listar():
    unidade_medida: Categoria = Categoria.query.all()
    return serialize(unidade_medida)
