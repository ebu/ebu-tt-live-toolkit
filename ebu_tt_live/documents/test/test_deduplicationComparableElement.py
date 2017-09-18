from unittest import TestCase
from ebu_tt_live.node import deduplicator
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.bindings import style_type, region_type, div_type, p_type, span_type, br_type, ebuttdt


class TestComparableElement(TestCase):

    test_style1 = style_type(
        id='SEQ58.defaultStyle1',
        direction='ltr',
        fontFamily='sansSerif',
        fontSize='1c 2c',
        lineHeight='normal',
        textAlign='left',
        color='rgb(255, 255, 255)',
        backgroundColor='rgb(0, 0, 0)',
        fontStyle='normal',
        fontWeight='normal',
        textDecoration='none',
        unicodeBidi='normal',
        wrapOption='wrap',
        padding='5px',
        multiRowAlign='center',
        linePadding='0.5c'
        )

    test_style2 = style_type(
        id='SEQ60.defaultStyle1',
        direction='ltr',
        fontFamily='sansSerif',
        fontSize='1c 2c',
        lineHeight='normal',
        textAlign='left',
        color='rgb(255, 255, 255)',
        backgroundColor='rgb(0, 0, 0)',
        fontStyle='normal',
        fontWeight='normal',
        textDecoration='none',
        unicodeBidi='normal',
        wrapOption='wrap',
        padding='5px',
        multiRowAlign='center',
        linePadding='0.5c'
        )

    test_style3 = style_type(
        id='SEQ59.defaultStyle1',
        direction='ltr',
        fontFamily='Serif',
        fontSize='1c 2c',
        lineHeight='normal',
        textAlign='left',
        color='rgb(0, 255, 255)',
        backgroundColor='rgb(0, 0, 0)',
        fontStyle='normal',
        fontWeight='normal',
        textDecoration='none',
        unicodeBidi='normal',
        wrapOption='wrap',
        padding='5px',
        multiRowAlign='center',
        linePadding='0.5c'
        )

    test_style4 = style_type(
        id='SEQ61.defaultStyle1',
        direction='ltr',
        fontSize='1c 2c',
        fontFamily='Serif',
        multiRowAlign='center',
        lineHeight='normal',
        textAlign='left',
        textDecoration='none',
        fontStyle='normal',
        fontWeight='normal',
        backgroundColor='rgb(0, 0, 0)',
        unicodeBidi='normal',
        color='rgb(0, 255, 255)',
        wrapOption='wrap',
        padding='5px',
        linePadding='0.5c'
        )
    comparableElement = deduplicator.ComparableElement

    def test_dup_elements_diff_ids(self):
        test_instance1 = self.comparableElement(self.test_style1)
        test_instance2 = self.comparableElement(self.test_style2)
        assert test_instance1.my_hash == test_instance2.my_hash

    def test_two_diff_elements(self):
        test_instance1 = self.comparableElement(self.test_style1)
        test_instance2 = self.comparableElement(self.test_style3)
        assert test_instance1.my_hash != test_instance2.my_hash

    def test_dup_elements_diff_order_attrs(self):
        test_instance1 = self.comparableElement(self.test_style3)
        test_instance2 = self.comparableElement(self.test_style4)
        assert test_instance1.my_hash == test_instance2.my_hash
