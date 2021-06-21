from sqlalchemy import String

from exts import db
from ..utils import Column, TimeRecordableCRUD


class Usuario(TimeRecordableCRUD, db.Model):
    __tablename__ = 'usuario'

    nome = Column(String(50))
    email = Column(String(50), unique=True)
    senha = Column(String(100))
