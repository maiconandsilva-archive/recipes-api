from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Text
from sqlalchemy_utils import ScalarListType, UUIDType
import typing as t

from lib.helpers import is_user_authenticated
from ..usuario.usuario import Usuario
from ..utils import BaseModel, Column, Describable, TimeRecordableCRUD
from .categoria import Categoria
from .ingrediente import Ingrediente
from .secondary import CategoriaReceita


@dataclass
class Receita(TimeRecordableCRUD, Describable, BaseModel):
    __tablename__ = 'receita'

    _MODO_PREPARO_SEP = '$'

    categorias: t.List[Categoria]
    ingredientes: t.List[Ingrediente]

    usuario_id: str = Column(UUIDType,
                             ForeignKey('usuario.id', ondelete='SET NULL'),
                             nullable=True)

    modo_preparo: str = Column(ScalarListType(separator=_MODO_PREPARO_SEP))
    tempo_preparo: int = Column(Integer)  # em minutos
    rendimento_porcoes: int = Column(Integer)
    observacoes: str = Column(Text, nullable=True)

    ingredientes = relationship('Ingrediente', backref='receita',
                                cascade="all, delete", passive_deletes=True)
    categorias = relationship('Categoria', secondary=CategoriaReceita,
                              backref='receitas')
    criador: Usuario = relationship('Usuario', backref='receitas')

    @validates('modo_preparo')
    def validate_modo_preparo(self, key, modo_preparo: dict):
        assert not any(self._MODO_PREPARO_SEP in step for step in modo_preparo)
        return modo_preparo

    @validates('criador', include_backrefs=False)
    def validate_criador(self, key, criador: Usuario):
        assert self.criador is None or self.criador is criador
        assert is_user_authenticated(criador)
        return criador
