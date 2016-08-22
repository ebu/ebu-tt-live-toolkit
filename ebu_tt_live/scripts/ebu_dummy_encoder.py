import logging
from datetime import timedelta

from ebu_tt_live.bindings import ebutt_live as bindings
from ebu_tt_live.bindings.ebutt_live import _ebuttdt as datatypes
from ebu_tt_live.bindings.ebutt_live import _ebuttm as metadata
from ebu_tt_live.documents.ebutt3 import EBUTT3Document
from pyxb import BIND

from .common import create_loggers

log = logging.getLogger('ebu_dummy_encoder')


def main():
    create_loggers()
    log.info('Dummy XML Encoder')

    tt = bindings.tt(
        sequenceIdentifier='testSequence001',
        sequenceNumber='1',
        timeBase='clock',
        clockMode='local',
        lang='en-GB',
        head=bindings.head_type(
            metadata.headMetadata_type(
                metadata.documentMetadata()
            ),
            bindings.styling(
                bindings.style(
                    id='ID001'
                )
            ),
            bindings.layout()
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
                )
            ),
            begin=datatypes.LimitedClockTimingType(timedelta(seconds=.5)),
            dur=datatypes.LimitedClockTimingType(timedelta(seconds=5))
        )
    )

    document = EBUTT3Document.create_from_raw_binding(tt)
    document.validate()

    print(
        document.get_xml()
    )

    log.info('XML output printed')
