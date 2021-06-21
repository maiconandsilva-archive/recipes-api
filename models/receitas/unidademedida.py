from sqlalchemy.sql.sqltypes import String

from exts import db
from ..utils import Column, Describable


class UnidadeMedida(Describable, db.Model):
    __tablename__ = 'unidade_medida'
    
    id = Column(String(20), primary_key=True)
