import dataclasses
import unittest

from src.json_automatic.a_composite_json_serializable import ACompositeJsonSerializable
from src.json_automatic.a_container_json_serializable import AContainerJsonSerializable
from src.json_automatic.raw_json import RawJson
from src.json_automatic.enum_json import EnumByNameJson, EnumByValueJson
from src.json_automatic.enum_named_objects import EnumNamedObjects
from src.json_automatic.i_json_serializable import IJsonSerializable
from src.json_automatic.named_object import NamedObject


class EnumTest(EnumByNameJson):
    VALUE1 = "4"
    VALUE2 = "10"


class EnumValueTest(EnumByValueJson):
    VALUE1 = "4"
    VALUE2 = "10"


@dataclasses.dataclass
class ContainerTest(AContainerJsonSerializable):
    __element_type__ = EnumTest
    elems: list[EnumTest] = dataclasses.field(default_factory=list)

    def __iter__(self):
        return iter(self.elems)

    def __eq__(self, other):
        return self.elems == other.elems

    def append(self, element):
        self.elems.append(element)


@dataclasses.dataclass
class ContainerValueTest(AContainerJsonSerializable):
    __element_type__ = EnumValueTest
    elems: list[EnumValueTest] = dataclasses.field(default_factory=list)

    def __iter__(self):
        return iter(self.elems)

    def __eq__(self, other):
        return self.elems == other.elems

    def append(self, element):
        self.elems.append(element)


@dataclasses.dataclass
class CompositeEnumTest(ACompositeJsonSerializable):
    value: int = 0
    en: EnumTest = EnumTest.VALUE1


class TestSerializationDeserialization(unittest.TestCase):

    def setUp(self) -> None:
        self.composite_with_enum = CompositeEnumTest(10, EnumTest.VALUE2)
        self.collection_empty = ContainerTest()
        self.collection = ContainerTest([EnumTest.VALUE1, EnumTest.VALUE1, EnumTest.VALUE2])
        self.arbitrary_json = RawJson([5, "str", {"dict": 10}])

    def test_cannot_create_fixed_container_with_different_types(self):
        self.assertRaises(ValueError, lambda: ContainerTest([EnumTest.VALUE1, EnumTest.VALUE1.value, "str"]))

    def test_composite(self):
        self.obj_test(self.composite_with_enum)

    def test_collection(self):
        self.obj_test(self.collection_empty)
        self.obj_test(self.collection)

    def test_arbitrary(self):
        self.obj_test(self.arbitrary_json)

    def test_value_enum(self):
        self.obj_test(ContainerValueTest([EnumValueTest.VALUE1, EnumValueTest.VALUE1, EnumValueTest.VALUE2]))

    def obj_test(self, obj: IJsonSerializable):
        j = obj.to_json()
        obj2 = obj.__class__.from_json(j)
        self.assertEqual(obj, obj2)
        
    def test_named_object_enum(self):
        class Tester(EnumNamedObjects):
            S1 = NamedObject("item", 1000)
        
        self.assertFalse(Tester.has_name("boi"))
        self.assertTrue(Tester.has_name("item"))
        self.assertEqual(Tester.S1.get_object(), 1000)
        self.assertEqual(Tester("item").get_object(), 1000)
