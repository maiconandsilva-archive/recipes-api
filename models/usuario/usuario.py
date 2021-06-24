from dataclasses import dataclass
from sqlalchemy import String
import sqlalchemy_utils as su
import uuid

from exts import db
from ..utils import Column, TimeRecordableCRUD


@dataclass
class Usuario(TimeRecordableCRUD, db.Model):
    __tablename__ = 'usuario'

    id: str = Column(su.UUIDType, primary_key=True, default=uuid.uuid4)
    nome: str = Column(String(255))
    email: str = Column(su.EmailType, unique=True)
    senha: su.Password = Column(su.PasswordType(schemes=['pbkdf2_sha512']))
