import typing as t


Callback = t.Callable[[str, t.Any], t.Dict]


def serialize(obj, *, ignore: Callback=None, mapdict: Callback=None,
              dict_factory=dict):
    """
    Convert dataclasses to dict recursevely in a json-like format through asdict.

    ignore: Remove the items which this function callback returns False
    mapdict: Map key, value pairs. The dictionary will have the the new values
             returned by the function
    dict_factory: If given, it will be used instead of built-in dict.
    """
    ...
