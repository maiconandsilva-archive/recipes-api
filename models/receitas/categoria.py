from dataclasses import dataclass

from ..utils import BaseModel, Describable


@dataclass
class Categoria(Describable, BaseModel):
    __tablename__ = 'categoria'

