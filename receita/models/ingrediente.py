import db
import sqlalchemy as sa
import sqlalchemy.orm as orm


class Ingrediente(db.Model):
    quantidade = sa.Column(sa.Integer)
    opcional = sa.Column(sa.Boolean, default=False)
    descricao = sa.Column(sa.String(400), nullable=True)
    base = orm.relationship('IngredienteBase')
    