from dataclasses import dataclass
from sqlalchemy.sql.sqltypes import String

from ..utils import BaseModel, Column, Describable


@dataclass
class UnidadeMedida(Describable, BaseModel):
    __tablename__ = 'unidade_medida'

    id: str = Column(String(20), primary_key=True)
