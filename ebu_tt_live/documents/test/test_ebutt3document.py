from unittest import TestCase
from datetime import timedelta, datetime
from ebu_tt_live.documents import EBUTT3Document,EBUTT3ObjectBase, EBUTTLiveMessage, EBUTTAuthorsGroupControlRequest
import os
import six
from ebu_tt_live.utils import compare_xml


class TestEBUTT3Document(TestCase):

    def test_comparison_same_sequence(self):
        document1 = EBUTT3Document("clock", 1, "testSeq", "en-GB", "local")
        document2 = EBUTT3Document("clock", 2, "testSeq", "en-GB", "local")
        self.assertTrue(document1 < document2)
        self.assertTrue(document2 > document1)
        self.assertTrue(document1 == document1)
        self.assertTrue(document1 <= document2)
        self.assertTrue(document2 >= document1)
        self.assertTrue(document1 <= document1)
        self.assertTrue(document1 >= document1)
        self.assertTrue(document1 != document2)
        self.assertTrue(document2 != document1)

    def test_comparison_different_sequences(self):
        document1 = EBUTT3Document("clock", 1, "testSeq1", "en-GB", "local")
        document2 = EBUTT3Document("clock", 2, "testSeq2", "en-GB", "local")
        # assertRaises does not catch the error correctly without the lambda.
        self.assertRaises(ValueError, lambda: document1 < document2)
        self.assertRaises(ValueError, lambda: document2 > document1)
        self.assertRaises(ValueError, lambda: document1 <= document2)
        self.assertRaises(ValueError, lambda: document2 >= document1)
        self.assertRaises(ValueError, lambda: document1 == document2)
        self.assertRaises(ValueError, lambda: document2 == document1)
        self.assertRaises(ValueError, lambda: document1 != document2)
        self.assertRaises(ValueError, lambda: document2 != document1)

    def test_availability_time(self):
        now = datetime.now()
        availability_time = timedelta(hours=now.hour, minutes=now.minute, seconds=now.second, microseconds=now.microsecond)
        document = EBUTT3Document("clock", 1, "testSeq1", "en-GB", "local")
        document.availability_time = availability_time
        self.assertEqual(document.availability_time, availability_time)
        # Only way to test the raising of an exception in a setter is  by using
        # this syntax and not the "=" syntax, because of the way the "="
        # operator works in python
        self.assertRaises(TypeError, lambda: document.availability_time(1))

    def test_is_equal_dom(self):
        xml = ""
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'document.xml')
        with open(file_path) as xml_file:
            xml = xml_file.read()
        document1 = EBUTT3Document.create_from_xml(xml)
        document2 = EBUTT3Document.create_from_xml(xml)
        self.assertTrue(compare_xml(document1.get_xml(), document2.get_xml()))
        document2 = EBUTT3Document.create_from_xml(xml.replace('500', '3500'))
        self.assertFalse(compare_xml(document2.get_xml(), document1.get_xml()))

    def test_live_message_instantiate(self):
        xml = ""
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'message.xml')
        with open(file_path) as xml_file:
            xml = xml_file.read()
        instance = EBUTT3ObjectBase.create_from_xml(xml)

        self.assertIsInstance(instance, EBUTTAuthorsGroupControlRequest)
        self.assertEqual(instance.sequence_identifier, 'TestSequence')
        self.assertEqual(instance.sender, 'testsender')
        self.assertEqual(instance.recipient, ['testrecipient1', 'testrecipient2'])
        self.assertEqual(instance.payload, 'This is a message for unittesting this messaging class.')

    def test_live_message_reserialize(self):
        xml = ""
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'message.xml')
        with open(file_path) as xml_file:
            xml = xml_file.read()
        instance = EBUTT3ObjectBase.create_from_xml(xml)

        re_xml = instance.get_xml()

        self.assertIsInstance(re_xml, six.text_type)
        self.assertTrue(compare_xml(xml, re_xml))
