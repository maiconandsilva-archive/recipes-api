from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer, String

from ..fractiontype import IntFractionType
from ..utils import BaseModel, Column, proxy_association_for
from .ingredienteinfo import IngredienteInfo
from .unidademedida import UnidadeMedida


@dataclass
class Ingrediente(BaseModel):
    __tablename__ = 'ingrediente'

    receita_id: int = Column(Integer, ForeignKey('receita.id', ondelete='CASCADE'))
    info_id: int = Column(Integer, ForeignKey(IngredienteInfo.id, ondelete='CASCADE'))

    quantidade: str = Column(String(50), default=1)
    opcional: bool = Column(Boolean, default=False)

    info: IngredienteInfo = relationship('IngredienteInfo', lazy='joined')

    __proxyinfo = proxy_association_for('info', IngredienteInfo)
    nome: str = __proxyinfo('nome')
    descricao: str = __proxyinfo('descricao')
    unidade_medida: UnidadeMedida = __proxyinfo('unidade_medida')
