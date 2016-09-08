
from unittest import TestCase
from datetime import timedelta
from ebu_tt_live.documents.converters import ebutt3_to_ebuttd
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.bindings import div_type, p_type, span_type, br_type, ebuttdt


class TestEBUTT3ToEBUTTDConverter(TestCase):

    def setUp(self):
        self._media_clock = MediaClock()

    def test_simple(self):
        div = div_type(
            p_type(
                span_type(
                    'Here we are',
                    br_type(),
                    'in 2 lines.'
                ),
                id='ID001',
                begin=ebuttdt.FullClockTimingType(timedelta(seconds=1)),
                end=ebuttdt.FullClockTimingType(timedelta(seconds=3))
            )
        )

        document = EBUTT3Document(
            time_base='media',
            lang='en-GB',
            sequence_identifier='TestSeq1',
            sequence_number=1
        )
        document.add_div(div)
        document.validate()

        ebutt3_to_ebuttd(document, self._media_clock)
