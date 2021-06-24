from dataclasses import dataclass
from datetime import datetime
from functools import wraps
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column as SAColumn
from sqlalchemy.sql.sqltypes import Integer, String, TIMESTAMP, Text

from exts import db
from .serialization import serialize


class Column(SAColumn):
    def params(self, *optionaldict, **kwargs):
        super().params(*optionaldict, **kwargs)

    def unique_params(self, *optionaldict, **kwargs):
        super().params(*optionaldict, **kwargs)

    @wraps(SAColumn.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)


@dataclass(init=False)
class BaseModel(db.Model):
    __abstract__ = True

    id: int = Column(Integer, primary_key=True, autoincrement=True)

    def save(self, commit=False):
        db.session.add(self)
        if commit:
            db.session.commit()

    def delete(self, commit=False):
        db.session.delete(self)
        if commit:
            db.session.commit()

    def serialize(self, **kwargs) -> dict:
        return serialize(self, **kwargs)


@dataclass(init=False)
class Describable:
    nome: str = Column(String(100))
    descricao: str = Column(Text, nullable=True)


@dataclass(init=False)
class TimeRecordableCRUD:
    created_on: datetime = Column(TIMESTAMP, server_default=func.now())
    last_updated_on: datetime = Column(TIMESTAMP, onupdate=func.now(),
                                       nullable=True)
    deleted_on: datetime = Column(TIMESTAMP, nullable=True)

    def isdeleted(self):
        return self.deleted_on is not None

    def soft_delete(self, commit=True):
        self.deleted_on = datetime.now()
        if commit:
            db.session.commit()


def proxy_association(target_collection: str, attr: str, Klass, **kw):
    return association_proxy(target_collection, attr,
                             creator=lambda value: Klass(**{attr: value}), **kw)


def proxy_association_for(target_collection: str, Klass):
    def wrapper(attr: str, **kw):
        return proxy_association(target_collection, attr, Klass, **kw)
    return wrapper
