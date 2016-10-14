
from unittest import TestCase
from datetime import timedelta
from ebu_tt_live import bindings
from ebu_tt_live.bindings import ebuttdt as datatypes
from ebu_tt_live.bindings import ebuttm as metadata
from ebu_tt_live.documents.converters import ebutt3_to_ebuttd
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.bindings import div_type, p_type, span_type, br_type, ebuttdt


class TestEBUTT3DocumentSegment(TestCase):

    def test_simple(self):
        tt = bindings.tt(
            sequenceIdentifier='testSequence001',
            sequenceNumber='1',
            timeBase='clock',
            extent='800px 600px',
            clockMode='local',
            lang='en-GB'
        )
        head_elem = bindings.head_type(
            metadata.headMetadata_type(
                metadata.documentMetadata()
            ),
            bindings.styling(
                bindings.style_type(
                    id='style1',
                    fontSize='12px'
                ),
                bindings.style_type(
                    id='style2',
                    fontSize='15px'
                ),
                bindings.style_type(
                    id='style3',
                    color='red',
                    fontSize='12px'
                )
            ),
            bindings.layout(
                bindings.region_type(
                    id='region1',
                    origin='200px 450px',
                    extent='300px 150px',
                    style=['style3']
                )
            )
        )
        body_elem = bindings.body_type(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Some example text...'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line'
                    ),
                    id='ID005',
                    begin=datatypes.LimitedClockTimingType(timedelta(seconds=.5)),
                    end=datatypes.LimitedClockTimingType(timedelta(seconds=3.42)),
                ),
                style=['style1'],
                region='region1'
            ),
            begin=datatypes.LimitedClockTimingType(timedelta(seconds=.5)),
            dur=datatypes.LimitedClockTimingType(timedelta(seconds=5)),
            style=['style2']
        )

        tt.head = head_elem
        tt.body = body_elem

        document = EBUTT3Document.create_from_raw_binding(binding=tt)
        document.validate()

        document.extract_segment(deconflict_ids=True)

    def test_trimmed_1(self):
        tt = bindings.tt(
            sequenceIdentifier='testSequence001',
            sequenceNumber='1',
            timeBase='clock',
            extent='800px 600px',
            clockMode='local',
            lang='en-GB'
        )
        head_elem = bindings.head_type(
            metadata.headMetadata_type(
                metadata.documentMetadata()
            ),
            bindings.styling(
                bindings.style_type(
                    id='style1',
                    fontSize='12px'
                ),
                bindings.style_type(
                    id='style2',
                    fontSize='15px'
                ),
                bindings.style_type(
                    id='style3',
                    color='red',
                    fontSize='12px'
                ),
                bindings.style_type(
                    id='style4',
                    backgroundColor='blue'
                )
            ),
            bindings.layout(
                bindings.region_type(
                    id='region1',
                    origin='200px 450px',
                    extent='300px 150px',
                    style=['style3']
                )
            )
        )
        body_elem = bindings.body_type(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Some example text...',
                        begin=datatypes.LimitedClockTimingType(timedelta(seconds=1)),
                        end=datatypes.LimitedClockTimingType(timedelta(seconds=2)),
                        style=['style4'],
                        id='span1'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line',
                        begin=datatypes.LimitedClockTimingType(timedelta(seconds=3)),
                        end=datatypes.LimitedClockTimingType(timedelta(seconds=4)),
                        id='span2'
                    ),
                    id='ID005'
                ),
                style=['style1'],
                region='region1'
            ),
            begin=datatypes.LimitedClockTimingType(timedelta(seconds=.5)),
            dur=datatypes.LimitedClockTimingType(timedelta(seconds=5)),
            style=['style2']
        )
        tt.head = head_elem
        tt.body = body_elem

        document = EBUTT3Document.create_from_raw_binding(binding=tt)
        document.validate()

        self.assertIsInstance(document.get_element_by_id('region1'), bindings.region_type)
        self.assertIsInstance(document.get_element_by_id('style1'), bindings.style_type)
        self.assertIsInstance(document.get_element_by_id('style2'), bindings.style_type)
        self.assertIsInstance(document.get_element_by_id('style3'), bindings.style_type)
        self.assertIsInstance(document.get_element_by_id('style4'), bindings.style_type)

        self.assertIsInstance(document.get_element_by_id('ID005'), bindings.p_type)
        self.assertIsInstance(document.get_element_by_id('span1'), bindings.span_type)
        self.assertIsInstance(document.get_element_by_id('span2'), bindings.span_type)

        cdoc = document.extract_segment(deconflict_ids=True, begin=timedelta(seconds=2.5))
        self.assertIsInstance(cdoc.get_element_by_id('SEQ1.region1'), bindings.region_type)
        self.assertIsInstance(cdoc.get_element_by_id('SEQ1.style1'), bindings.style_type)
        self.assertIsInstance(cdoc.get_element_by_id('SEQ1.style2'), bindings.style_type)
        self.assertIsInstance(cdoc.get_element_by_id('SEQ1.style3'), bindings.style_type)
        self.assertRaises(LookupError, cdoc.get_element_by_id, 'SEQ1.style4')

        self.assertIsInstance(cdoc.get_element_by_id('SEQ1.ID005'), bindings.p_type)
        self.assertRaises(LookupError, cdoc.get_element_by_id, 'SEQ1.span1')
        self.assertIsInstance(cdoc.get_element_by_id('SEQ1.span2'), bindings.span_type)
