from unittest import TestCase
from ebu_tt_live.documents import EBUTT3DocumentSequence
from mock import patch, MagicMock


class TestEBUTT3DocumentSequence(TestCase):

    @patch('ebu_tt_live.clocks.Clock')
    def test_produces_valid_documents(self, clock_mock):
        clock_mock.clock_mode = MagicMock(return_value="local")
        clock_mock.time_base = MagicMock(return_value="clock")
        testSeq = EBUTT3DocumentSequence("test", clock_mock, 'en-GB')
        document = testSeq.new_document()


