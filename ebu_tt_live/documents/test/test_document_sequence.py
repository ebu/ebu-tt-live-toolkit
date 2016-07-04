from unittest import TestCase
from ebu_tt_live.documents import EBUTT3DocumentSequence
from mock import patch


class TestEBUTT3DocumentSequence(TestCase):

    @patch("ebu_tt_live.clocks.base.Clock")
    def test_produces_valid_documents(self, clock_mock):
        clock_mock.clock_mode = "local"
        clock_mock.time_base = "clock"
        testSeq = EBUTT3DocumentSequence("test", clock_mock, "en-GB")
        document = testSeq.new_document()
        self.assertEqual(document._ebutt3_content.timeBase, "clock")
        self.assertEqual(document._ebutt3_content.clockMode, "local")
        self.assertEqual(document.sequence_identifier, "test")
        self.assertEqual(document._ebutt3_content.lang, "en-GB")
        document.validate()

    @patch("ebu_tt_live.clocks.base.Clock")
    def test_increases_sequence_number(self, clock_mock):
        clock_mock.clock_mode = "local"
        clock_mock.time_base = "clock"
        testSeq = EBUTT3DocumentSequence("test", clock_mock, "en-GB")
        document1 = testSeq.new_document()
        document2 = testSeq.new_document()
        assert document2.sequence_number > document1.sequence_number
