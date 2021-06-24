import sqlalchemy.orm as orm

import exts
from .serialization import Callback


class BaseModel(exts.db.Model):
    query: orm.Query
    session: orm.Session

    def serialize(self, *, ignore: Callback=None, mapdict: Callback=None,
                  dict_factory=dict) -> dict: ...
