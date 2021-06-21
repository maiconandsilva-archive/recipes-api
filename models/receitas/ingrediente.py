from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Boolean, Integer

from exts import db
from ..utils import Column, proxy_association_for
from .ingredienteinfo import IngredienteInfo


class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'

    receita_id = Column(Integer, ForeignKey('receita.id', ondelete='CASCADE'))
    info_id = Column(Integer, ForeignKey(IngredienteInfo.id, ondelete='CASCADE'))

    quantidade = Column(Integer, default=1)
    opcional = Column(Boolean, default=False)

    info = relationship('IngredienteInfo', lazy='joined')

    __proxyinfo = proxy_association_for('info', IngredienteInfo)
    nome = __proxyinfo('nome')
    descricao = __proxyinfo('descricao')
    unidade_medida = __proxyinfo('unidade_medida')
