
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import Integer

from exts import db
from ..utils import Column, Describable


class Categoria(Describable, db.Model):
    __tablename__ = 'categoria'

