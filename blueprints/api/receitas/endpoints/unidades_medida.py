from models.receitas import UnidadeMedida
from models.serialization import serialize
from ..blueprint import unidades_medida


@unidades_medida.route('/')
def listar():
    unidade_medida: UnidadeMedida = UnidadeMedida.query.all()
    return serialize(unidade_medida)
