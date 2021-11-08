import dataclasses
import unittest
import json

from src.json_annotated.a_composite_json_serializable import ACompositeJsonSerializable
from src.json_annotated.raw_json import RawJson
from src.json_annotated.enum_json import EnumByNameJson, EnumByValueJson
from src.json_annotated.enum_named_objects import EnumNamedObjects
from src.json_annotated.i_json_serializable import IJsonSerializable
from src.json_annotated.named_object import NamedObject


class EnumTest(EnumByNameJson):
    VALUE1 = "4"
    VALUE2 = "10"


class EnumValueTest(EnumByValueJson):
    VALUE1 = "4"
    VALUE2 = "10"


@dataclasses.dataclass
class CompositeEnumTest(ACompositeJsonSerializable):
    value: int = 0
    en: EnumTest = EnumTest.VALUE1
    ls: list[EnumTest] = dataclasses.field(default_factory=list)

    def __eq__(self, other):
        return self.value == other.value and \
                self.en == other.en and \
                self.ls == other.ls


class TestSerializationDeserialization(unittest.TestCase):

    def setUp(self) -> None:
        self.composite_with_enum = CompositeEnumTest(10, EnumTest.VALUE2, [EnumTest.VALUE2, EnumTest.VALUE1])
        self.arbitrary_json = RawJson([5, "str", {"dict": 10}])

    def test_composite(self):
        self.obj_test(self.composite_with_enum)

    def test_arbitrary(self):
        self.obj_test(self.arbitrary_json)

    def test_named_object_enum(self):
        class Tester(EnumNamedObjects):
            S1 = NamedObject("item", 1000)

        self.assertFalse(Tester.has_name("boi"))
        self.assertTrue(Tester.has_name("item"))
        self.assertEqual(Tester.S1.get_object(), 1000)
        self.assertEqual(Tester("item").get_object(), 1000)
        
    def obj_test(self, obj: IJsonSerializable):
        j = obj.to_json()
        obj2 = obj.__class__.from_json(j)
        self.assertEqual(obj, obj2)
        self.assertEqual(obj.__class__.from_json(json.loads(json.dumps(obj.to_json()))), obj)
