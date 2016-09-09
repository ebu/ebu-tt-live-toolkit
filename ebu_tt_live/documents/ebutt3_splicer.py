
from datetime import timedelta
import logging
import copy
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import tt


log = logging.getLogger(__name__)


class EBUTT3Splicer(object):

    _document_segments = None
    _sequence_identifier = None
    _sequence_number = None
    _spliced_document = None
    _dataset = None

    def __init__(self, document_segments, sequence_identifier, sequence_number):
        if not document_segments:
            raise Exception()
        self._document_segments = list(reversed(list(document_segments)))
        self._sequence_identifier = sequence_identifier
        self._sequence_number = sequence_number
        self._dataset = {
            'ids': set()
        }
        self._do_splice()

    @property
    def spliced_document(self):
        return self._spliced_document

    def _do_splice(self):

        first_doc = self._document_segments.pop()
        first_tt = first_doc.binding

        merged_tt = first_tt
        merged_head = first_tt.head
        merged_styling = first_tt.head.styling
        merged_layout = first_tt.head.layout

        merged_body = first_tt.body

        while self._document_segments:
            current_doc = self._document_segments.pop()
            current_tt = current_doc.binding
            merged_tt = merged_tt.merge(current_tt, self._dataset)

            if merged_head:
                merged_head = merged_head.merge(current_tt.head, self._dataset)
                if merged_styling:
                    merged_styling = merged_styling.merge(current_tt.head.styling, self._dataset)
                else:
                    merged_styling = current_tt.head.styling
                if merged_layout:
                    merged_layout = merged_layout.merge(current_tt.head.layout, self._dataset)
                else:
                    merged_layout = current_tt.head.layout
            else:
                merged_head = current_tt.head

            if merged_body:
                merged_body = merged_body.merge(current_tt.body, self._dataset)
            else:
                merged_body = current_tt.body

        merged_head.layout = merged_layout
        merged_head.styling = merged_styling

        merged_tt.head = merged_head
        merged_tt.body = merged_body

        merged_tt.sequenceIdentifier = self._sequence_identifier
        merged_tt.sequenceNumber = self._sequence_number

        merged_tt._setElement(tt)

        self._spliced_document = merged_tt
