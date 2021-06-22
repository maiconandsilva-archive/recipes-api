from dataclasses import dataclass
from sqlalchemy import String

from exts import db
from ..utils import Column, TimeRecordableCRUD


@dataclass
class Usuario(TimeRecordableCRUD, db.Model):
    __tablename__ = 'usuario'

    nome: str = Column(String(50))
    email: str = Column(String(50), unique=True)
    senha: str = Column(String(100))
