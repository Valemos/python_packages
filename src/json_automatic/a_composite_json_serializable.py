from .i_json_serializable import IJsonSerializable
from .metaclasses import CompositeJsonScheme


class ACompositeJsonSerializable(IJsonSerializable, metaclass=CompositeJsonScheme):
    """Only annotated attributes will be serialized"""

    def to_json(self):
        result = {}
        for attr in self.__class__.__serialized__:
            value = getattr(self, attr)
            if attr in self.__serializable_children__:
                result[attr] = value.to_json()
            elif IJsonSerializable.is_basic_type(type(value)):
                result[attr] = value
            else:
                raise ValueError(f'cannot serialize "{attr}"')
        return result

    @classmethod
    def from_json(cls, json_object: dict):
        obj = cls()
        for attr in cls.__serialized__:
            json_child = json_object[attr]
            if attr in cls.__serializable_children__:
                setattr(obj, attr, cls.__serializable_children__[attr].from_json(json_child))
            else:
                setattr(obj, attr, json_child)
        return obj
