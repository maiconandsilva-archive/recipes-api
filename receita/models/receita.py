import db
import sqlalchemy as sa
import sqlalchemy.orm as orm


class Receita(db.Model):
    nome = sa.Column(sa.String(50))
    modo_preparo = sa.Column(sa.String(1000))
    ingredientes = orm.relationship('Ingrediente', secondary='receita_ingredientes')
    
    