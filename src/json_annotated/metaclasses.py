import inspect
import typing
from typing import Type, Optional

from .i_json_serializable import IJsonSerializable


class CompositeJsonScheme(type):
    __serialized__: tuple
    __ignored__: tuple
    __serializable_children__: dict
    __serializable_arrays__: dict

    def __init__(cls, name, bases, namespace) -> None:
        super().__init__(name, bases, namespace)
        if not hasattr(cls, "__ignored__"):
            cls.__ignored__ = tuple()

        cls._initialize_scheme()

    def _initialize_scheme(cls):
        cls.__serialized__ = tuple(cls.__annotations__.keys())
        cls.__serializable_children__ = {}
        cls.__serializable_arrays__ = {}
        for attr in cls.__serialized__:
            if attr in cls.__ignored__: continue
            attr_type = cls._get_annotation_type(attr)

            if IJsonSerializable.is_serializable_type(attr_type):
                cls.__serializable_children__[attr] = attr_type
                continue

            type_origin = typing.get_origin(attr_type)
            if type_origin is None: continue
            if issubclass(type_origin, list):
                elem_type = typing.get_args(attr_type)[0]
                if IJsonSerializable.is_serializable_type(elem_type):
                    cls.__serializable_arrays__[attr] = type_origin, elem_type

    @staticmethod
    def _get_fields_iter(obj):
        for member_name, _ in inspect.getmembers(obj, lambda x: not (inspect.isroutine(x))):
            if not member_name.startswith("__") and member_name not in obj.__class__.__ignored__:
                yield member_name

    def _get_annotation_type(cls, attribute) -> Optional[Type]:
        if attribute in cls.__annotations__:
            return cls.__annotations__[attribute]
        return None
