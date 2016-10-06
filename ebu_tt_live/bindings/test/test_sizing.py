
from unittest import TestCase
from ebu_tt_live.bindings import ebuttdt


class TestPixelFontSizeType(TestCase):

    _test_string_1 = '10px'
    _test_string_2 = '10px 20px'
    _type_class = ebuttdt.PixelFontSizeType

    def test_simple_1dim(self):
        test_instance = self._type_class(self._test_string_1)
        self.assertIsNone(test_instance.horizontal)
        self.assertEquals(test_instance.vertical, 10.0)
        self.assertEquals(test_instance, self._test_string_1)

    def test_simple_2dim(self):
        test_instance = self._type_class(self._test_string_2)
        self.assertEquals(test_instance.horizontal, 10.0)
        self.assertEquals(test_instance.vertical, 20.0)
        self.assertEquals(test_instance, self._test_string_2)

    def test_instantiate_1dim(self):
        test_instance = self._type_class(10)
        self.assertIsNone(test_instance.horizontal)
        self.assertEquals(test_instance.vertical, 10.0)
        self.assertEquals(test_instance, self._test_string_1)

    def test_instantiate_2dim(self):
        test_instance = self._type_class(10, 20)
        self.assertEquals(test_instance.horizontal, 10.0)
        self.assertEquals(test_instance.vertical, 20.0)
        self.assertEquals(test_instance, self._test_string_2)


class TestCellFontSizeType(TestPixelFontSizeType):

    _test_string_1 = '10c'
    _test_string_2 = '10c 20c'
    _type_class = ebuttdt.CellFontSizeType


class TestPercentageFontSizeType(TestPixelFontSizeType):

    _test_string_1 = '10%'
    _test_string_2 = '10% 20%'
    _type_class = ebuttdt.PercentageFontSizeType
