import logging
from .common import create_loggers
from ebu_tt_live import bindings
from ebu_tt_live.bindings import _ebuttm as metadata
from pyxb import BIND

log = logging.getLogger('ebu_dummy_encoder')


def main():
    create_loggers()
    log.info('Dummy XML Encoder')

    tt = bindings.tt(
        sequenceIdentifier='testSequence001',
        sequenceNumber='1',
        timeBase='smpte',
        lang='en-GB',
        head=bindings.head(
            metadata.headMetadata(
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
            bindings.div(
                bindings.p(
                    bindings.span(
                        'Some example text...'
                    ),
                    bindings.br(),
                    bindings.span(
                        'And another line'
                    ),
                    id='ID005',
                    begin='00:00:00:50',
                    end='00:00:03:24',
                )
            )
        )
    )

    print(
        tt.toDOM().toprettyxml(
            indent='  '
        )
    )
    log.info('XML output printed')
