
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import String

from exts import db
from ..utils import Column, Describable
from .unidademedida import UnidadeMedida

class IngredienteInfo(Describable, db.Model):
    """
    Esta classe vai ser usada como uma parte da classe Ingrediente.
    Foi separada para ser possível fazer a pesquisa de ingredientes
    e nao precisar duplicar informacoes.
    """

    __tablename__ = 'ingrediente_info'

    unidade_id = Column(String(20), ForeignKey('unidade_medida.id'))
    unidade_medida = relationship('UnidadeMedida')
