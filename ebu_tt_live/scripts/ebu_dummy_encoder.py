import logging
from .common import create_loggers
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings import _ebuttdt as datatypes
from ebu_tt_live.bindings import load_types_for_document
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from pyxb import BIND
from datetime import timedelta, datetime

log = logging.getLogger('ebu_dummy_encoder')


def main():
    create_loggers(logging.INFO)
    log.info('Dummy XML Encoder')

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
                id='ID005',
            ),
            style=['style1'],
            region='region1'
        ),
        begin=datatypes.LimitedClockTimingType(timedelta(seconds=.5)),
        dur=datatypes.LimitedClockTimingType(timedelta(seconds=5)),
        style=['style2']
    )

    applied_proc1 = metadata.appliedProcessing_type(
        process='Creation',
        generatedBy='ebu_dummy_encoder',
        appliedDateTime=datetime.now())
    
    applied_proc2 = metadata.appliedProcessing_type(
        process='Validation',
        generatedBy='ebu_dummy_encoder',
        appliedDateTime=datetime.now())
    
    head_elem.metadata.documentMetadata.appliedProcessing.append(applied_proc1)
    head_elem.metadata.documentMetadata.appliedProcessing.append(applied_proc2)
    tt.head = head_elem
    tt.body = body_elem

    document = EBUTT3Document.create_from_raw_binding(tt)

    document.validate()

    print((
        document.get_xml()
    ))

    log.info('XML output printed')
