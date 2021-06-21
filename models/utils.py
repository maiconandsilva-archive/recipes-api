from datetime import datetime
from functools import wraps
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import Column as SAColumn
from sqlalchemy.sql.sqltypes import String, TIMESTAMP, Text

from exts import db


class Column(SAColumn):
    @wraps(SAColumn.__init__)
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('nullable', False)
        super().__init__(*args, **kwargs)


class Describable:
    nome = Column(String(50))
    descricao = Column(Text, nullable=True)


class TimeRecordableCRUD:
    created_on = Column(TIMESTAMP, server_default=func.now())
    last_updated_on = Column(TIMESTAMP, onupdate=func.now(), nullable=True)
    deleted_on = Column(TIMESTAMP, nullable=True)

    def isdeleted(self):
        return self.deleted_on is not None

    def soft_delete(self, commit=True):
        self.deleted_on = datetime.now()
        if commit:
            db.session.commit()


def proxy_association(target_collection, attr, Klass, **kw):
    return association_proxy(target_collection, attr,
                             creator=lambda value: Klass(**{attr: value}), **kw)


def proxy_association_for(target_collection, Klass):
    def wrapper(attr, **kw):
        return proxy_association(target_collection, attr, Klass, **kw)
    return wrapper
