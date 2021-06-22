from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Text
import typing as t

from ..usuario.usuario import Usuario
from ..utils import BaseModel, Column, Describable, TimeRecordableCRUD
from .categoria import Categoria
from .ingrediente import Ingrediente
from .secondary import CategoriaReceita


@dataclass
class Receita(TimeRecordableCRUD, Describable, BaseModel):
    __tablename__ = 'receita'

    categorias: t.List[Categoria]
    ingredientes: t.List[Ingrediente]

    usuario_id: int = Column(Integer, ForeignKey('usuario.id', ondelete='SET NULL'),
                             nullable=True)

    modo_preparo: str = Column(Text)
    ingredientes = relationship('Ingrediente', backref='receita',
                                cascade="all, delete", passive_deletes=True)
    categorias = relationship('Categoria', secondary=CategoriaReceita,
                              backref='receitas')
    criador: Usuario = relationship('Usuario', backref='receitas')
