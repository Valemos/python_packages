from copy import deepcopy
from enum import Enum
from typing import Union

from .named_object import NamedObject


class EnumNamedObjects(Enum):

    _value_: Union[NamedObject, str]

    def get_object(self):
        if hasattr(self.value, "item"):
            return deepcopy(self.value.item)
        else:
            return self.value

    @classmethod
    def has_name(cls, name):
        return any(name == key for key, _ in cls._value2member_map_.items())


