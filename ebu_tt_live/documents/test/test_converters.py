from unittest import TestCase
from datetime import timedelta
import os
from ebu_tt_live.documents.converters import ebutt3_to_ebuttd, ebutt1_to_ebutt3
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.documents.ebutt1 import EBUTT1Document
from ebu_tt_live.clocks.media import MediaClock
from ebu_tt_live.bindings import tt1_head_type, styling, \
    style_type, tt1_layout_type, region_type, div_type, p_type, \
    span_type, br_type, ebuttdt
from pyxb.exceptions_ import PyXBException


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

    def test_ericsson_3(self):

        xml_file = self._load_asset('converter_ericsson3.xml')

        self._media_clock.adjust_time(
            timedelta(),
            ebuttdt.LimitedClockTimingType('12:11:50.000').timedelta)

        document = EBUTT3Document.create_from_xml(xml_file)
        ebutt3_to_ebuttd(document, self._media_clock)


class TestEBUTT1ToEBUTT3Converter(TestCase):

    def setUp(self):
        self._seqId = 'testConverter'

    def _load_asset(self, file_name):
        dirpath = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(dirpath, file_name), 'r') as ifile:
            contents = ifile.read()
            return contents

    def test_simple_smpte(self):

        div = div_type(
            p_type(
                span_type(
                    'Here we are',
                    br_type(),
                    'in 2 lines.'
                ),
                id='ID001',
                begin=ebuttdt.SMPTETimingType('00:00:01:00'),
                end=ebuttdt.SMPTETimingType('00:00:03:00')
            )
        )

        EBUTT1Document.load_types_for_document()
        try:
            document = EBUTT1Document(
                time_base='smpte',
                lang='en-GB',
                head=tt1_head_type(
                    styling(
                        style_type(id='s0')
                    ),
                    tt1_layout_type(
                        region_type(
                            id='r0',
                            origin='0% 0%',
                            extent='100% 100%')
                    )
                )
            )
        except PyXBException as e:
            print(e.details())
            raise e
        document.add_div(div)
        document.validate()

        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True)

    def test_simple_media(self):

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

        EBUTT1Document.load_types_for_document()
        try:
            document = EBUTT1Document(
                time_base='media',
                lang='en-GB',
                head=tt1_head_type(
                    styling(
                        style_type(id='s0')
                    ),
                    tt1_layout_type(
                        region_type(
                            id='r0',
                            origin='0% 0%',
                            extent='100% 100%')
                    )
                )
            )
        except PyXBException as e:
            print(e.details())
            raise e
        document.add_div(div)
        document.validate()

        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True)

    def test_ericsson_smpte(self):

        xml_file = self._load_asset('converter_ericsson1_smpte.xml')

        document = EBUTT1Document.create_from_xml(xml_file)
        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True)

    def test_ericsson_smpte_with_start_of_programme(self):

        xml_file = self._load_asset(
            'converter_ericsson1_smpte_with_start_of_programme.xml')

        document = EBUTT1Document.create_from_xml(xml_file)
        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True)

    def test_ericsson_smpte_with_start_of_programme_and_sub_zero(self):

        xml_file = self._load_asset(
            'converter_ericsson1_smpte_with_start_of_programme_and_sub_zero.xml')  # noqa:E501

        document = EBUTT1Document.create_from_xml(xml_file)
        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True)

    def test_ericsson_smpte_with_overridden_start_of_programme(self):

        xml_file = self._load_asset(
            'converter_ericsson1_smpte_with_start_of_programme.xml')

        document = EBUTT1Document.create_from_xml(xml_file)
        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True,
            smpte_start_of_programme='11:00:00:00')

    def test_ericsson_smpte_with_overridden_start_of_programme_and_sub_zero(
            self):

        xml_file = self._load_asset(
            'converter_ericsson1_smpte_with_start_of_programme_and_sub_zero.xml')  # noqa:E501

        document = EBUTT1Document.create_from_xml(xml_file)
        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True,
            smpte_start_of_programme='11:00:00:00')

    def test_ericsson_media(self):

        xml_file = self._load_asset('converter_ericsson1_media.xml')

        document = EBUTT1Document.create_from_xml(xml_file)
        ebutt1_to_ebutt3(
            document,
            sequence_id=self._seqId,
            use_doc_id_as_seq_id=True)
