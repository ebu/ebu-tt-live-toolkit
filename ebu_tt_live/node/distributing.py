from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3Document
import logging
import six

log = logging.getLogger(__name__)


class DistributingNode(AbstractCombinedNode):

    _reference_clock = None
    _expects = EBUTT3Document
    _provides = six.text_type

    def __init__(self, node_id, producer_carriage=None, consumer_carriage=None, **kwargs):
        super(DistributingNode, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage,
            **kwargs
        )

    def process_document(self, document, raw_xml=None, **kwargs):
        if self.is_document(document):
            if self.check_if_document_seen(document) is True:
                if raw_xml is not None:
                    data = raw_xml
                else:
                    data = document.get_xml()
                self.producer_carriage.emit_data(data=data, **kwargs)
            else:
                log.warning(
                    'Ignoring duplicate document: {}__{}'.format(
                        document.sequence_identifier,
                        document.sequence_number
                    )
                )
        else:
            self.producer_carriage.emit_data(data=document.get_xml(), **kwargs)
