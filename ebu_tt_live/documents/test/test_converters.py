
from unittest import TestCase
from datetime import timedelta
import os
from ebu_tt_live.documents.converters import ebutt3_to_ebuttd
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.clocks.local import LocalMachineClock
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.bindings import div_type, p_type, span_type, br_type, ebuttdt


class TestEBUTT3ToEBUTTDConverter(TestCase):

    def setUp(self):
        self._media_clock = MediaClock()

    def _load_asset(self, file_name):
        dirpath = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirpath, file_name), 'r') as ifile:
            contents = ifile.read()
            return contents

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

    def test_ericsson_1(self):

        xml_file = self._load_asset('converter_ericsson1.xml')

        self._media_clock.adjust_time(timedelta(), ebuttdt.LimitedClockTimingType('12:11:50.000').timedelta)

        document = EBUTT3Document.create_from_xml(xml_file)
        cdoc = ebutt3_to_ebuttd(document, self._media_clock)
