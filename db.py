from sqlalchemy import event, DDL
from sqlalchemy.engine import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.session import Session, sessionmaker


class SQLAlchemy:
    def __init__(self, app=None, **kwargs):
        self.Model = declarative_base(name='Model')
        if app:
            self.init_app(app, **kwargs)

    def init_app(self, app, **kwargs):
        kwargs.setdefault('autocommit', False)
        kwargs.setdefault('autoflush', False)
        kwargs.setdefault('engine_cfg', {})

        self.__make_session(**kwargs)

        query: Query = self.session.query_property()

        self.Model.query = query
        self.Model.session = self.session

        self.__add_db_hooks_to_app(app)

    def drop_all(self):
        self.delete_schemas()
        self.Model.metadata.drop_all(bind=self.engine)

    def delete_schemas(self):
        pass

    def create_all(self):
        self.create_schemas()
        self.Model.metadata.create_all(bind=self.engine)

    def create_schemas(self):
        for mapper in self.Model.registry.mappers:
            cls = mapper.class_
            if issubclass(cls, self.Model):
                table_args = getattr(cls, '__table_args__', None)
                if table_args:
                    schema = table_args.get('schema')
                    if schema:
                        query = f"CREATE SCHEMA IF NOT EXISTS {schema}"
                        event.listen(
                            self.Model.metadata, 'before_create', DDL(query))

    def __add_db_hooks_to_app(self, app):
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            self.session.remove()

    def __make_session(self, **kwargs):
        self.engine = create_engine(kwargs.pop('dburi'),
                                    **kwargs.pop('engine_cfg'))
        self.SessionLocal = sessionmaker(bind=self.engine, **kwargs)
        self.session: Session = scoped_session(
            self.SessionLocal, scopefunc=kwargs.pop('scopefunc', None))
