import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session


class BaseModelMeta(DeclarativeMeta):
    @property
    def session(self):
        if '__bind_key__' in self:
            return self._sessions[self.__bind_key__]
        return self._session
        
    def save(self, commit=False):
        self.add(self)
        if commit:
            self.commit()
    
    def delete(self, commit=False):
        self.session.delete(self)
        if commit:
            self.commit()
        
    def __getattr__(self, name):
        attr = getattr(self.session, name)
        if callable(attr):
            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)
            return wrapper
        return attr    


class SQLAlchemy:
    def __init__(self, app=None, scopefunc=None, **kwargs):
        self.Model = declarative_base(metaclass=BaseModelMeta)
        if app:
            self.init_app(app, scopefunc, **kwargs)
    
    def init_app(self, app, **kwargs):
        dburi = app.config.get('SQLALCHEMY_DATABASE_URI')
        binds = app.config.get('SQLALCHEMY_BINDS', {}).copy()
        kwargs.setdefault('autocommit', False)
        kwargs.setdefault('autoflush', False)
        kwargs.get('connect_args', {}).setdefault('check_same_thread', False)
        
        for key, uri in binds:
            binds[key] = self.__make_session(uri, **kwargs)
        self.Model._sessions = binds
        self.Model._session = self.__make_session(dburi, **kwargs)

    def __make_session(self, dburi, **kwargs):
        SessionLocal = sessionmaker(create_engine(dburi, **kwargs), **kwargs)
        return scoped_session(SessionLocal, scopefunc=kwargs.get('scopefunc'))