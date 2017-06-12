from .base import AbstractCombinedNode
from ebu_tt_live.documents import EBUTT3DocumentSequence, EBUTT3Document
from ebu_tt_live.bindings import _ebuttm as metadata
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation, StopBranchIteration
from ebu_tt_live.strings import DOC_RECEIVED
from ebu_tt_live.errors import SequenceNumberCollisionError
from ebu_tt_live.errors import UnexpectedSequenceIdentifierError
from pyxb.binding.basis import NonElementContent, ElementContent
from pyxb import BIND
from ebu_tt_live import bindings
import logging


log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


class DeDuplicatorNode(AbstractCombinedNode):
    _original_styles = []
    _new_style_list = [[],[],[],[]]
    _styling_element = None
    _region_element = None
    _span_style_id = None
    _region_style_id = None
    _sequence_identifier = None
    # _sequence_number = None
    _expects = EBUTT3Document
    _provides = EBUTT3Document

    def __init__(self, node_id, sequence_identifier, consumer_carriage=None, producer_carriage=None):
        super(DeDuplicatorNode, self).__init__(
            node_id=node_id,
            consumer_carriage=consumer_carriage,
            producer_carriage=producer_carriage
        )
        self._sequence_identifier = sequence_identifier
        # self._sequence_number = sequence_number

    def process_document(self, document, **kwargs):
        if self.is_document(document):

            if document.sequence_identifier == self._sequence_identifier:
                raise UnexpectedSequenceIdentifierError()

            if self.check_if_document_seen(document=document):

                self.limit_sequence_to_one(document)

                # change the sequence identifier and sequence number
                document.sequence_identifier = self._sequence_identifier
                #document.sequence_number = self._sequence_number

                document.validate()
                self.producer_carriage.emit_data(data=document, **kwargs)

    def remove_duplication(self, document, original_styles, new_style_list, styling_element, region_element, span_style_id, region_style_id):

        for style in document.tt.head.styling:
            


        original_styles =   [
                                bindings.style_type(   id='SEQ58.defaultStyle1',
                                                        color='rgb(255,255,255)',
                                                        backgroundColor='rgb(0,0,0)'),

                                bindings.style_type(   id='SEQ59.defaultStyle1',
                                                        color='rgb(255,255,255)',
                                                        backgroundColor='rgb(0,0,0)')

                                # [bindings.style_type(   id= 'SEQ60.defaultStyle1',
                                #                         color= 'rgb(0,255,255)',
                                #                         backgroundColor= 'rgb(0,0,0)')]
                            ]

        list_a = [[],[]]
        list_b = [[],[]]
        new_style_list = [[],[],[],[]]

        i = 0

        list_a[0].append(original_styles[i].color)
        list_a[1].append(original_styles[i].backgroundColor)

        for x in range(len(original_styles)):
            list_b[0].append(original_styles[x].color)
            list_b[1].append(original_styles[x].backgroundColor)

            if list_a == list_b:
                new_style_list[0].append(original_styles[i].id)
                new_style_list[1].append(original_styles[i].color)
                new_style_list[2].append(original_styles[i].backgroundColor)

        for y in range(len(new_style_list[0])):
            new_style_list[3].append("style" + str(y))
