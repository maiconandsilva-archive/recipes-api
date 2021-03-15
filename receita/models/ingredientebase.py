import db
import sqlalchemy as sa

class IngredienteBase(db.Model):
    nome = sa.Column(sa.String(25))
    unidade = sa.Column(sa.String(30))
    