from unittest import TestCase
from ebu_tt_live import bindings
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation
from ebu_tt_live.bindings import ebuttdt as datatypes
from ebu_tt_live.bindings import ebuttm as metadata
from ebu_tt_live.node import deduplicator
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.bindings import load_types_for_document


class TestReplaceStylesAndRegions(TestCase):
        load_types_for_document('ebutt3')
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
                    id='SEQ58.defaultStyle1',
                    fontSize='12px',
                    color='rgb(255,255,255)',
                    backgroundColor='rgb(0,0,0)',
                    fontFamily='sansSerif'
                ),
                bindings.style_type(
                    id='SEQ59.defaultStyle1',
                    fontSize='12px',
                    color='rgb(255,255,255)',
                    backgroundColor='rgb(0,0,0)',
                    fontFamily='sansSerif'
                ),
                bindings.style_type(
                    id='SEQ60.defaultStyle1',
                    fontSize='12px',
                    color='rgb(0,255,255)',
                    backgroundColor='rgb(0,0,0)',
                    fontFamily='sansSerif'
                ),
                bindings.style_type(
                    id='SEQ61.defaultStyle1',
                    fontSize='12px',
                    color='rgb(255,255,255)',
                    backgroundColor='rgb(0,0,0)',
                    fontFamily='sansSerif'
                )
            ),
            bindings.layout(
                bindings.region_type(
                    id='SEQ58.bottomRegion1',
                    origin='14.375% 60%',
                    extent='71.25% 24%',
                    style=['SEQ58.defaultStyle1']
                ),
                bindings.region_type(
                    id='SEQ59.bottomRegion1',
                    origin='14.375% 60%',
                    extent='71.25% 24%',
                    style=['SEQ58.defaultStyle1']
                ),
                bindings.region_type(
                    id='SEQ60.bottomRegion1',
                    origin='14.375% 60%',
                    extent='71.25% 24%',
                    style=['SEQ58.defaultStyle1']
                ),
                bindings.region_type(
                    id='SEQ61.bottomRegion1',
                    origin='14.375% 60%',
                    extent='71.25% 24%',
                    style=['SEQ58.defaultStyle1']
                )
            )
        )
        body_elem = bindings.body_type(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Some example text...',
                        style=['SEQ58.defaultStyle1'],
                        id='span1'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line',
                        style=['SEQ58.defaultStyle1'],
                        id='span2'
                    ),
                    id='ID005'
                ),
                region='SEQ58.bottomRegion1'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Another example text...',
                        style=['SEQ59.defaultStyle1'],
                        id='span3'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line',
                        style=['SEQ59.defaultStyle1'],
                        id='span4'
                    ),
                    id='ID006'
                ),
                region='SEQ59.bottomRegion1'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'More example text...',
                        style=['SEQ60.defaultStyle1'],
                        id='span5'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line',
                        style=['SEQ60.defaultStyle1'],
                        id='span6'
                    ),
                    id='ID007'
                ),
                region='SEQ60.bottomRegion1'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Further example text...',
                        style=['SEQ61.defaultStyle1'],
                        id='span7'
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'And another line',
                        style=['SEQ61.defaultStyle1'],
                        id='span8'
                    ),
                    id='ID008'
                ),
                region='SEQ61.bottomRegion1'
            ),
        )

        tt.head = head_elem
        tt.body = body_elem

        test_old_ids = ({'SEQ58.defaultStyle1': 1, 'SEQ59.defaultStyle1': 2, 'SEQ60.defaultStyle1': 3, 'SEQ61.defaultStyle1': 4, 'SEQ58.bottomRegion1': 5, 'SEQ59.bottomRegion1': 6, 'SEQ60.bottomRegion1': 7, 'SEQ61.bottomRegion1': 8 })
        test_new_ids = ({1: 'SEQ61.defaultStyle1', 3: 'SEQ60.defaultStyle1', 5: 'SEQ61.bottomRegion1'})

        replaceStylesAndRegions = deduplicator.ReplaceStylesAndRegions

        def test_one(self):
            document = EBUTT3Document.create_from_raw_binding(binding=self.tt)
            document.validate()

            cdoc = self.replaceStylesAndRegions(document, self.test_old_ids, self.test_new_ids)
            cdoc.proceed()

            document.validate()

            print(document.get_xml())
