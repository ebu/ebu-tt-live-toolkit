from unittest import TestCase
import os
from ebu_tt_live.utils import compare_xml
from ebu_tt_live.documents import EBUTT1Document
from pyxb.exceptions_ import UnrecognizedAttributeError


class TestEBUTT1Document(TestCase):
    def test_is_equal_dom(self):
        xml = ""
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'document_ebutt1.xml')
        with open(file_path) as xml_file:
            xml = xml_file.read()
        document1 = EBUTT1Document.create_from_xml(xml)
        document2 = EBUTT1Document.create_from_xml(xml)
        self.assertTrue(compare_xml(document1.get_xml(), document2.get_xml()))
        document2 = EBUTT1Document.create_from_xml(xml.replace('500', '3500'))
        self.assertFalse(compare_xml(document2.get_xml(), document1.get_xml()))

    def test_sequence_number_disallowed(self):
        # Load the EBUTT3 document as EBUTT1. This should fail because EBUTT1 doesn't have a sequenceNumber attribute
        xml = ""
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'document.xml')
        with open(file_path) as xml_file:
            xml = xml_file.read()

        self.assertRaises(
            UnrecognizedAttributeError,
            EBUTT1Document.create_from_xml,
            xml
        )
