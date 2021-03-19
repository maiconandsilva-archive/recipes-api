from sqlalchemy import Column, ForeignKey
from sqlalchemy import Integer, Boolean, String
from sqlalchemy.orm import relationship

from exts import db


class Ingrediente(db.Model):
    __tablename__ = 'ingrediente'
    __table_args__ = {
        'schema': 'receitas'
    }

    receita_id = Column(Integer, ForeignKey('receitas.receita.id'))
    info_id = Column(Integer, ForeignKey('receitas.ingrediente_info.id'))

    quantidade = Column(Integer)
    opcional = Column(Boolean, default=False)
    descricao = Column(String(400), nullable=True)

    info = relationship('IngredienteInfo')

    def __getattr__(self, name):
        """
        Acessa propriedades da classe IngredienteInfo.
        Uma maneira de nao precisar digitar Ingrediente.info
        """
        return getattr(self.info, name)
