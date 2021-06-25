from typing import List
from flask import abort
from models.receitas.receita import Receita

from models.receitas import Categoria
from models.serialization import serialize
from ..blueprint import bp_categorias


@bp_categorias.route('/')
def listar():
    unidade_medida: List[Categoria] = Categoria.query.all()
    return serialize(unidade_medida)


@bp_categorias.route('/<int:categoria_id>')
def listar_receitas_por_categoria(categoria_id: int):
    categoria: Categoria = Categoria.query.get(categoria_id)
    receitas: List[Receita]

    if categoria is None:
        abort(404)

    receitas = Receita.query.filter_by(categoria=categoria).all()
    return serialize(receitas)
