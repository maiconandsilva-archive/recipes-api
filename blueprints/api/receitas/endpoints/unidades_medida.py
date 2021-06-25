from typing import List

from models.receitas import UnidadeMedida
from models.serialization import serialize
from ..blueprint import bp_unidades_medida


@bp_unidades_medida.route('/')
def listar():
    unidade_medida: List[UnidadeMedida] = UnidadeMedida.query.all()
    return serialize(unidade_medida)
