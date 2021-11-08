
from .i_json_serializable import IJsonSerializable
from .metaclasses import CompositeJsonScheme


class ACompositeJsonSerializable(IJsonSerializable, metaclass=CompositeJsonScheme):
    """Only annotated attributes will be serialized"""

    def to_json(self):
        result = {}
        for attr in self.__class__.__serialized__:
            value = getattr(self, attr)
            if attr in self.__serializable_children__:
                result[attr] = IJsonSerializable._object_to_json(value)
            elif attr in self.__serializable_arrays__:
                result[attr] = [IJsonSerializable._object_to_json(element) for element in value]
            else:
                raise ValueError(f'cannot serialize "{attr}"')
        return result

    @classmethod
    def from_json(cls, json_object: dict):
        obj = cls()
        for attr in cls.__serialized__:
            json_child = json_object[attr]
            if attr in cls.__serializable_children__:
                element_type = cls.__serializable_children__[attr]
                setattr(obj, attr, cls._object_from_json(element_type, json_child))

            elif attr in cls.__serializable_arrays__:
                array_type, element_type = cls.__serializable_arrays__[attr]
                setattr(obj, attr, array_type(cls._object_from_json(element_type, el) for el in json_child))
            else:
                raise ValueError('cannot deserialize, schema changed!')

        return obj
