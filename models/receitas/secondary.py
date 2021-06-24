
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer

from ..utils import BaseModel

CategoriaReceita = Table('categoria_receita', BaseModel.metadata,
    Column('receita_id', Integer, ForeignKey('receita.id'), primary_key=True),
    Column('categoria_id', Integer, ForeignKey('categoria.id'), primary_key=True),
)
