from sqlalchemy.orm.query import Query
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer

import exts


class Base:
    id: int = Column(Integer, primary_key=True, autoincrement=True)

    def save(self, commit=False):
        exts.db.session.add(self)
        if commit:
            exts.db.session.commit()

    def delete(self, commit=False):
        exts.db.session.delete(self)
        if commit:
            exts.db.session.commit()
