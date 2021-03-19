from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

from exts import db


class Receita(db.Model):
    __tablename__ = 'receita'
    __table_args__ = {
        'schema': 'receitas'
    }

    usuario_id = Column(Integer, ForeignKey('usuarios.usuario.id'))
    nome = Column(String(50))
    modo_preparo = Column(String(1000))
    ingredientes = relationship('Ingrediente',
                                secondary='receitas.receita_ingredientes')

    # Criador das receitas
    usuario = relationship('Usuario', backref='receitas')
