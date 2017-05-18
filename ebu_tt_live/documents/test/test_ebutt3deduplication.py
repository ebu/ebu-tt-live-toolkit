from unittest import TestCase
from datetime import timedelta
from ebu_tt_live import bindings
from ebu_tt_live.bindings import ebuttdt as datatypes
from ebu_tt_live.bindings import ebuttm as metadata
from ebu_tt_live.documents.converters import ebutt3_to_ebuttd
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from ebu_tt_live.bindings import div_type, p_type, span_type, br_type, ebuttdt

class TestEBUTT3DocumentDeDuplication(TestCase):

    def test_input_file(self):
        tt = bindings.tt(
            sequenceIdentifier='testSequence001',
            sequenceNumber='1'
        )
        head_elem = bindings.head_type(
            metadata.headMetadata_type(
                metadata.documentMetadata()
            ),
            bindings.styling(
                bindings.style_type(
                    id='SEQ58.defaultStyle1',
                    linePadding='0.5c',
                    backgroundColor='rgb(0, 0, 0)',
                    color='rgb(255, 255, 255)',
                    fontFamily='sansSerif'
                ),
                bindings.style_type(
                    id='SEQ59.defaultStyle1',
                    linePadding='0.5c',
                    backgroundColor='rgb(0, 0, 0)',
                    color='rgb(255, 255, 255)',
                    fontFamily='sansSerif'
                ),
                bindings.style_type(
                    id='SEQ60.defaultStyle1',
                    linePadding='0.5c',
                    backgroundColor='rgb(0, 0, 0)',
                    color='rgb(255, 255, 255)',
                    fontFamily='sansSerif'
                )
            ),
            bindings.layout(
                bindings.region_type(
                    id='SEQ58.bottomRegion',
                    displayAlign='after',
                    extent='71.25% 24%',
                    origin='14.375% 60%',
                    overflow='visible',
                    writingMode='lrtb'
                ),
                bindings.region_type(
                    id='SEQ59.bottomRegion',
                    displayAlign='after',
                    extent='71.25% 24%',
                    origin='14.375% 60%',
                    overflow='visible',
                    writingMode='lrtb'
                ),
                bindings.region_type(
                    id='SEQ560.bottomRegion',
                    displayAlign='after',
                    extent='71.25% 24%',
                    origin='14.375% 60%',
                    overflow='visible',
                    writingMode='lrtb'
                )
            )
        )
        body_elem = bindings.body_type(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Multiply your anger by about a'
                        style=['SEQ58.defaultStyle1']
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'hundred, Kate, that\'s how much he'
                        style=['SEQ58.defaultStyle1']
                    ),
                    id='SEQ58.ID001.1'
                ),
                region='SEQ58.bottomRegion'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'thinks he loves you.'
                        style=['SEQ59.defaultStyle1']
                    ),
                    id='SEQ59.ID001.1'
                ),
                region='SEQ59.bottomRegion'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Multiply your anger by about a'
                        style=['SEQ60.defaultStyle1']
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'hundred, Kate, that\'s how much he'
                        style=['SEQ60.defaultStyle1']
                    ),
                    id='SEQ60.ID001.1'
                ),
                region='SEQ60.bottomRegion'
            )
        )

        tt.head = head_elem
        tt.body = body_elem

        document = EBUTT3Document.create_from_raw_binding
        document.validate()

    def test_deduplicated_file(self):
        tt = bindings.tt(
            sequenceIdentifier='testSequence001',
            sequenceNumber='1'
        )
        head_elem = bindings.head_type(
            metadata.headMetadata_type(
                metadata.documentMetadata()
            ),
            bindings.styling(
                bindings.style_type(
                    id='defaultStyle1',
                    linePadding='0.5c',
                    backgroundColor='rgb(0, 0, 0)',
                    color='rgb(255, 255, 255)',
                    fontFamily='sansSerif'
                )
            ),
            bindings.layout(
                bindings.region_type(
                    id='bottomRegion',
                    displayAlign='after',
                    extent='71.25% 24%',
                    origin='14.375% 60%',
                    overflow='visible',
                    writingMode='lrtb'
                )
            )
        )
        body_elem = bindings.body_type(
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Multiply your anger by about a'
                        style=['defaultStyle1']
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'hundred, Kate, that\'s how much he'
                        style=['defaultStyle1']
                    ),
                    id='SEQ58.ID001.1'
                ),
                region='bottomRegion'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'thinks he loves you.'
                        style=['defaultStyle1']
                    ),
                    id='SEQ59.ID001.1'
                ),
                region='bottomRegion'
            ),
            bindings.div_type(
                bindings.p_type(
                    bindings.span_type(
                        'Multiply your anger by about a'
                        style=['defaultStyle1']
                    ),
                    bindings.br_type(),
                    bindings.span_type(
                        'hundred, Kate, that\'s how much he'
                        style=['defaultStyle1']
                    ),
                    id='SEQ60.ID001.1'
                ),
                region='bottomRegion'
            )
        )
        tt.head = head_elem
        tt.body = body_elem

        document = EBUTT3Document.create_from_raw_binding
        document.validate()

        self.assertIsInstance(document.get_element_by_id('bottomRegion'), bindings.region_type)
        self.assertIsInstance(document.get_element_by_id('defaultStyle1'), bindings.style_type)
