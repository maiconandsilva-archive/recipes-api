from sqlalchemy import Column
from sqlalchemy import String

from exts import db


class Usuario(db.Model):
    __tablename__ = 'usuario'    
    __table_args__ = {
        'schema': 'usuarios'
    }
    
    email = Column(String(50), unique=True)
    senha = Column(String(100))
