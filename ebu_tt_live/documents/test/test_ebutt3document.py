from unittest import TestCase
from datetime import timedelta, datetime
from ebu_tt_live.documents import EBUTT3Document


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
