from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from exts import db


class IngredienteInfo(db.Model):
    """
    Esta classe vai ser usada como uma parte da classe Ingrediente.
    Foi separada para ser possível fazer a pesquisa de ingredientes
    e nao precisar duplicar informacoes.
    """

    __tablename__ = 'ingrediente_info'
    __table_args__ = {
        'schema': 'receitas'
    }

    unidade_id = Column(Integer, ForeignKey('receitas.unidade.id'))
    nome = Column(String(25))
    unidade = relationship('Unidade')
