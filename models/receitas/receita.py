from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer, Text

from exts import db
from ..utils import Column, Describable, TimeRecordableCRUD
from .secondary import CategoriaReceita

class Receita(TimeRecordableCRUD, Describable, db.Model):
    __tablename__ = 'receita'

    usuario_id = Column(Integer, ForeignKey('usuario.id', ondelete='SET NULL'),
                        nullable=True)

    modo_preparo = Column(Text)
    ingredientes = relationship('Ingrediente', backref='receita',
                                cascade="all, delete", passive_deletes=True)
    categorias = relationship('Categoria', secondary=CategoriaReceita,
                              backref='receitas')
    criador = relationship('Usuario', backref='receitas')
