from dataclasses import dataclass, is_dataclass, asdict
from datetime import datetime
from functools import wraps
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import session
from sqlalchemy.orm.query import Query
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column as SAColumn
from sqlalchemy.sql.sqltypes import String, TIMESTAMP, Text

from exts import db


class BaseModel(db.Model):
    __abstract__ = True

    query: Query
    session: session.Session

    def asdict(self) -> dict:
        assert is_dataclass(self), \
            'You need to add the @dataclass anotation to %s' % self.__class__
        return asdict(self)


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
