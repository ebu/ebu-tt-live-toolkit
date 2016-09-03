import logging
from .common import create_loggers
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings import _ebuttdt as datatypes
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from pyxb import BIND
from datetime import timedelta

log = logging.getLogger('ebu_dummy_encoder')


def main():
    create_loggers()
    log.info('Dummy XML Encoder')

    tt = bindings.tt(
        sequenceIdentifier='testSequence001',
        sequenceNumber='1',
        timeBase='clock',
        extent='800px 600px',
        clockMode='local',
        lang='en-GB',
        head=bindings.head_type(
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
        ),
        body=BIND(
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
    )

    document = EBUTT3Document.create_from_raw_binding(tt)

    document.validate()

    print(
        document.get_xml()
    )

    log.info('XML output printed')
    log.info('p applicable styles are as follows: {}'.format(document.binding.body.div[0].p[0].validated_styles))
