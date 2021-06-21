
from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.sql.sqltypes import Integer

from exts import db


CategoriaReceita = Table('categoria_receita', db.Model.metadata,
    Column('receita_id', Integer, ForeignKey('receita.id'), primary_key=True),
    Column('categoria_id', Integer, ForeignKey('categoria.id'), primary_key=True),
)
