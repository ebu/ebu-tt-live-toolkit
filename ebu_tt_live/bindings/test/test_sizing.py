
from unittest import TestCase
from ebu_tt_live.bindings import ebuttdt

class TestPixelFontSizeType(TestCase):

    def test_simple_1dim(self):
        test_string = '10px'
        test_instance = ebuttdt.PixelFontSizeType(test_string)
        self.assertIsNone(test_instance.horizontal)
        self.assertEquals(test_instance.vertical, 10.0)
        self.assertEquals(test_instance, test_string)

    def test_simple_2dim(self):
        test_string = '10px 20px'
        test_instance = ebuttdt.PixelFontSizeType(test_string)
        self.assertEquals(test_instance.horizontal, 10.0)
        self.assertEquals(test_instance.vertical, 20.0)
        self.assertEquals(test_string, test_instance)


class TestCellFontSizeType(TestCase):

    def test_simple_1dim(self):
        test_string = '10c'
        test_instance = ebuttdt.CellFontSizeType(test_string)
        self.assertIsNone(test_instance.horizontal)
        self.assertEquals(test_instance.vertical, 10.0)
        self.assertEquals(test_instance, test_string)

    def test_simple_2dim(self):
        test_string = '10c 20c'
        test_instance = ebuttdt.CellFontSizeType(test_string)
        self.assertEquals(test_instance.horizontal, 10.0)
        self.assertEquals(test_instance.vertical, 20.0)
        self.assertEquals(test_string, test_instance)


class TestPercentageFontSizeType(TestCase):

    def test_simple_1dim(self):
        test_string = '10%'
        test_instance = ebuttdt.PercentageFontSizeType(test_string)
        self.assertIsNone(test_instance.horizontal)
        self.assertEquals(test_instance.vertical, 10.0)
        self.assertEquals(test_instance, test_string)

    def test_simple_2dim(self):
        test_string = '10% 20%'
        test_instance = ebuttdt.PercentageFontSizeType(test_string)
        self.assertEquals(test_instance.horizontal, 10.0)
        self.assertEquals(test_instance.vertical, 20.0)
        self.assertEquals(test_string, test_instance)