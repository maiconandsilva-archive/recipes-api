# from _typeshed import Self
from _typeshed import Self
from blueprints.errorhandlers.exceptions import NotFoundException
from crypt import methods
from dataclasses import is_dataclass
import functools
from uuid import UUID

from sqlalchemy.orm import session
import typing as t
from flask.blueprints import Blueprint
from flask.globals import g, request

from models.serialization import serialize, serialized
from models.usuario.usuario import Usuario
from models.utils import BaseModel, Describable


def is_user_authenticated(user: Usuario = None):
    if user is None:
        return session.get('usuario_id') is not None
    return session.get('usuario_id') == user.id


class Searcheable:
    search_url = '/search'

    def search(self, query: str) -> NotImplemented:
        return NotImplemented


class SearcheableDescribableBase(Searcheable, Describable, BaseModel):
    def search(self, query: str) -> t.List['SearcheableDescribableBase']:
        cls: t.Type[SearcheableDescribableBase] = type(self)
        self.query.filter(cls.nome.ilike('%{}%'.format(query))).all()


IdType = t.Union[int, str, UUID]
Schema = t.ClassVar[t.Union[BaseModel, Searcheable]]
''.title().replace('-', ' ')


@API
class Resource:
    def __init__(self, schema: BaseModel):
        if not is_dataclass(schema):
            raise TypeError('The schema needs to be a dataclass')

        self.schema = schema

    def register_blueprint(self, blueprint: Blueprint):
        pass

    @query
    def get(self, id: IdType):
        return self.schema.query.get(id)

    @query
    def all(self):
        return self.schema.query.all()

    @query
    def search(self, query: str) -> t.List[BaseModel]:
        if isinstance(self.schema, Searcheable):
            return self.schema.search(query)
        raise NotFoundException

    @mutation.create
    def create(self):
        model = self.schema()
        model.from_json(request.json)
        model.validate()
        return model

    @mutation.bulk_update
    def bulk_update(self, ids: t.List[IdType]):
        pass

    @mutation.update
    def update(self, id: IdType):
        return self.bulk_update([id])

    @mutation.bulk_delete
    def bulk_delete(self, ids: t.List[IdType]):
        return self.schema.query.filter(self.schema.id.in_(ids)).delete()

    @mutation.delete
    def delete(self, id: IdType):
        return self.bulk_delete([id])


class ResourceBlueprint(Blueprint):
    _RULE = '/'
    _RULE_RESOURCE = '<id>'

    schemas = []

    def route(self, rule: str, **options: t.Any) -> t.Callable:
        defroute = super().route(rule, **options)
        if options.pop('serialized', True):
            return defroute(serialized)
        return defroute

    def add_resource(self, schema: Schema, url_prefix: str = None, mutable=True,
                     **options):
        _rule = url_prefix or self._RULE
        _resource_rule = _rule + self._RULE_RESOURCE

        self.schemas.append(schema)
        resource = schema

        if not isinstance(schema, Resource):
            resource = Resource(schema)

        resource.register_blueprint(self)
        # self.add_url_rule(_rule, view_func=resource.all)
        # self.add_url_rule(_resource_rule, view_func=resource.get)
        # self.add_url_rule(_rule, view_func=resource.get)
        # self.add_url_rule(_rule, view_func=resource.get)


        # @self.route(_rule)
        # def get_all(self, ):
        #     return self.schema.query.all()

        # @self.route(_resource_rule)
        # def get(self, id: IdType):
        #     return self.schema.query.get(id)

        # if isinstance(self.schema, Searcheable):
        #     @self.route(f'{_rule}/{self.schema.search_url}/<query>')
        #     def search(query: str) -> t.List[BaseModel]:
        #         return self.schema.search(query)

        # if mutable:
        #     @self.route(_rule, methods=['POST'])
        #     def create(self, ):
        #         model = self.schema()
        #         model.from_json(request.json)
        #         model.validate()
        #         return model

            # @self.route(_rule, methods=['POST'])
        #     def update(self, id: IdType):
        #         self.schema.query.get(id)

        #     @self.route(_resource_rule, methods=['DELETE'])
        #     def delete(self, id: IdType):
        #         return self.schema.delete(commit=True)
