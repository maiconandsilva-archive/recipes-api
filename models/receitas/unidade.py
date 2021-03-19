from sqlalchemy import Column
from sqlalchemy import String

from exts import db


class Unidade(db.Model):
    __tablename__ = 'unidade'
    __table_args__ = {
        'schema': 'receitas'
    }

    nome = Column(String(30))
    descricao = Column(String(100))
