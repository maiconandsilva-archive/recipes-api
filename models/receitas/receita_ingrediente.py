from sqlalchemy import Column, Table, ForeignKey, Integer

from exts import db


receita_ingredientes = Table('receita_ingredientes', db.Model.metadata,
    Column('ingrediente_id', Integer, ForeignKey('receitas.ingrediente.id')),
    Column('receita_id', Integer, ForeignKey('receitas.receita.id')),
    schema='receitas',
)
