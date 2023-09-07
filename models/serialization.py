from dataclasses import asdict, is_dataclass, make_dataclass
from functools import partial
import functools
import typing as t


def _g_ignore(prop: t.Tuple[str, t.Any]):
    """Global properties ignore for serialization."""
    key, value = prop
    return not (
        value is None
        or key in ('senha',)
        or key.endswith('_id')
    )


def _g_map(prop):
    """Global mapping for serialization."""
    return prop


def _dictfactory(properties: t.List, /, *, ignore=None, mapdict=None,
                 global_ignore=None, global_mapdict=None,
                 dict_factory: t.Callable = dict) -> dict:
    props = properties.copy()

    if global_ignore:
        props = filter(global_ignore, props)

    if ignore:
        props = filter(ignore, props)

    if global_mapdict:
        props = map(global_mapdict, props)

    if mapdict:
        props = map(mapdict, props)

    return dict_factory(props)


_DummyDataclass = make_dataclass('DummyDataclass', ('container',))


def _serialize(obj, /, **kwargs) -> dict:
    if not is_dataclass(obj):
        obj = _DummyDataclass(container=obj)
    return asdict(obj, dict_factory=partial(_dictfactory, **kwargs))



import typing as t


Callback = t.Callable[[str, t.Any], t.Dict]


def serialize(obj, /, *, ignore: Callback = None, mapdict: Callback = None,
              dict_factory=dict):
    """
    Convert dataclasses to dict recursevely in a json-like format through asdict.

    ignore: Remove the items which this function callback returns False
    mapdict: Map key, value pairs. The dictionary will have the the new values
             returned by the function
    dict_factory: If given, it will be used instead of built-in dict.
    """
    return _serialize(obj, ignore, mapdict, global_ignore=_g_ignore,
                      global_mapdict=_g_map, dict_factory=dict_factory)


def serialized(f: t.Callable) -> t.Callable:
    """Decorator for serialing the returned results from a function."""
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return serialize(f(*args, **kwargs))
    return wrapper
