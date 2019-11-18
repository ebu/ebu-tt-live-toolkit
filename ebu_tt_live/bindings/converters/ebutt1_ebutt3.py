from ebu_tt_live.bindings import tt, tt1_tt_type, tt1_body_type, \
    body_type, div_type, tt1_head_type, tt1_layout_type, p_type, span_type,  \
    br_type, head_type, style_type, styling, layout, \
    region_type, load_types_for_document
from ebu_tt_live.bindings._ebuttm import headMetadata_type, documentMetadata, \
    metadataBase_type, divMetadata_type
from ebu_tt_live.bindings._ebuttdt import FullClockTimingType
from ebu_tt_live.errors import TimeNegativeError
from ebu_tt_live.strings import ERR_TIME_NEGATIVE
from pyxb.binding.basis import NonElementContent, ElementContent
from datetime import timedelta
import copy
import logging

log = logging.getLogger(__name__)


class EBUTT1EBUTT3Converter(object):
    """
    Class to convert EBU-TT-1 documents into EBU-TT-3 documents.

    Includes a setting to extract the document identifier from metadata
    and use it as the output sequence identifier, or can just use a
    provided sequence identifier. The sequence number is always 1.
    """

    _semantic_dataset = None
    _sequenceIdentifier = None
    _use_doc_id_as_seq_id = False

    def __init__(self, sequence_id, use_doc_id_as_seq_id=False):
        """
        Construct a converter.

        :param sequence_id:
        :param use_doc_id_as_seq_id:
        """
        self._sequenceIdentifier = sequence_id
        self._use_doc_id_as_seq_id = use_doc_id_as_seq_id

    def map_type(self, in_element):
        if isinstance(in_element, tt1_tt_type):
            return self.convert_tt
        elif isinstance(in_element, tt1_head_type):
            return self.convert_head
        elif isinstance(in_element, tt1_body_type):
            return self.convert_body
        elif isinstance(in_element, div_type):
            return self.convert_div
        elif isinstance(in_element, p_type):
            return self.convert_p
        elif isinstance(in_element, span_type):
            return self.convert_span
        elif isinstance(in_element, br_type):
            return self.convert_br
        elif isinstance(in_element, tt1_layout_type):
            return self.convert_layout
        elif isinstance(in_element, region_type):
            return self.convert_region
        elif isinstance(in_element, styling):
            return self.convert_styling
        elif isinstance(in_element, style_type):
            return self.convert_style
        elif isinstance(in_element, headMetadata_type):
            return self.convert_headMetadata
        elif isinstance(in_element, divMetadata_type):
            return self.convert_divMetadata
        elif isinstance(in_element, metadataBase_type):
            return self.convert_metadata
        else:
            return self.convert_unknown

    def convert_tt(self, tt_in, dataset):
        dataset['timeBase'] = tt_in.timeBase
        new_elem = tt(
            head=self.convert_element(tt_in.head, dataset),
            body=self.convert_element(tt_in.body, dataset),
            timeBase='media',
            lang=tt_in.lang,
            space=tt_in.space,
            cellResolution=tt_in.cellResolution,
            sequenceIdentifier=self._sequenceIdentifier,
            sequenceNumber='1',
            _strict_keywords=False
        )

        if self._use_doc_id_as_seq_id and 'documentIdentifier' in dataset:
            new_elem.sequenceIdentifier = dataset['documentIdentifier']

        return new_elem

    def convert_head(self, head_in, dataset):
        new_elem = head_type()
        head_children = self.convert_children(head_in, dataset)
        for item in head_children:
            new_elem.append(item)

        return new_elem

    def convert_headMetadata(self, headMetadata_in, dataset):
        new_elem = headMetadata_type(
            *self.convert_children(headMetadata_in, dataset)
        )

        # Special handling for conformsToStandard. Throw out the old, add a
        # new.
        # TODO: When XSD updated to allow ebuttm document metadata directly in
        # head metadata, check for this by uncommenting the following lines:
        # if new_elem.conformsToStandard is not None:
        #     new_elem.conformsToStandard=[
        #         'urn:ebu:tt:live:2017-05']
        if new_elem.documentMetadata is None:
            new_elem.documentMetadata = documentMetadata(conformsToStandard=[
                'urn:ebu:tt:live:2017-05'
            ])
        else:
            new_elem.documentMetadata.conformsToStandard = [
                'urn:ebu:tt:live:2017-05']

        # We want to remember the documentIdentifier and use it later for the
        # sequence identifier
        # TODO: When XSD updated to allow ebuttm document metadata directly in
        # head metadata, check for this by uncommenting the following lines:
        # if new_elem.documentIdentifier is not None:
        #     _rememberDocumentIdentifier(new_elem.documentIdentifier, dataset)

        if new_elem.documentMetadata and \
           new_elem.documentMetadata.documentIdentifier is not None:
            self._rememberDocumentIdentifier(
                new_elem.documentMetadata.documentIdentifier,
                dataset)

        return new_elem

    def _rememberDocumentIdentifier(self, documentIdentifier_in, dataset):
        if 'documentIdentifier' in dataset:
            raise Exception('Already got a documentIdentifier')
        dataset['documentIdentifier'] = documentIdentifier_in

    def convert_divMetadata(self, divmetadata_in, dataset):
        new_elem = divMetadata_type(
            *self.convert_children(divmetadata_in, dataset)
        )
        return new_elem

    def convert_metadata(self, metadata_in, dataset):
        new_elem = metadataBase_type(
            *self.convert_children(metadata_in, dataset)
        )
        return new_elem

    def convert_styling(self, styling_in, dataset):
        new_elem = styling(
            *self.convert_children(styling_in, dataset)
        )
        return new_elem

    def convert_style(self, style_in, dataset):
        new_elem = style_type(
            *self.convert_children(style_in, dataset),
            id=style_in.id,
            style=style_in.style,
            direction=style_in.direction,
            fontFamily=style_in.fontFamily,
            fontSize=style_in.fontSize,
            lineHeight=style_in.lineHeight,
            textAlign=style_in.textAlign,
            color=style_in.color,
            backgroundColor=style_in.backgroundColor,
            fontStyle=style_in.fontStyle,
            fontWeight=style_in.fontWeight,
            textDecoration=style_in.textDecoration,
            unicodeBidi=style_in.unicodeBidi,
            wrapOption=style_in.wrapOption,
            padding=style_in.padding,
            multiRowAlign=style_in.multiRowAlign,
            linePadding=style_in.linePadding,
            _strict_keywords=False
        )
        return new_elem

    def convert_layout(self, layout_in, dataset):
        new_elem = layout(
            *self.convert_children(layout_in, dataset)
        )

        return new_elem

    def convert_region(self, region_in, dataset):
        new_elem = region_type(
            *self.convert_children(region_in, dataset),
            id=region_in.id,
            origin=region_in.origin,
            extent=region_in.extent,
            style=region_in.style,
            displayAlign=region_in.displayAlign,
            padding=region_in.padding,
            writingMode=region_in.writingMode,
            showBackground=region_in.showBackground,
            overflow=region_in.overflow,
            _strict_keywords=False
        )
        return new_elem

    def calculate_times(self, elem_in, dataset):
        begin = elem_in.begin
        end = elem_in.end

        if dataset['timeBase'] == 'smpte':
            syncbase = dataset['syncbase'][-1]

            if begin is not None:
                begin = dataset['smpte_to_timebase_converter'].timedelta(begin)
                if begin < syncbase:
                    raise TimeNegativeError(ERR_TIME_NEGATIVE)
                begin = begin - syncbase
            if end is not None:
                end = dataset['smpte_to_timebase_converter'].timedelta(end)
                if end < syncbase:
                    raise TimeNegativeError(ERR_TIME_NEGATIVE)
                end = end - syncbase
        else:
            if begin is not None:
                begin = begin.timedelta
            if end is not None:
                end = end.timedelta

        return begin, end

    def push_syncbase(self, dataset, sync_delta):
        if sync_delta is None:
            dataset['syncbase'].append(dataset['syncbase'][-1])
        else:
            dataset['syncbase'].append(dataset['syncbase'][-1] + sync_delta)

    def pop_syncbase(self, dataset):
        dataset['syncbase'].pop()

    def convert_body(self, body_in, dataset):
        if len(body_in.div) == 0:
            return None

        # Set up a syncbase list for use down the tree
        dataset['syncbase'] = [timedelta(seconds=0)]

        try:
            begin, end = self.calculate_times(body_in, dataset)
        except TimeNegativeError:
            return None

        self.push_syncbase(dataset, begin)

        if begin is not None:
            begin = FullClockTimingType(begin)
        if end is not None:
            end = FullClockTimingType(end)

        new_elem = body_type(
            *self.convert_children(body_in, dataset),
            agent=body_in.agent,
            role=body_in.role,
            style=body_in.style,
            begin=begin,
            end=end
        )

        self.pop_syncbase(dataset)

        if len(new_elem.orderedContent()) == 0:
            new_elem = None

        return new_elem

    def convert_div(self, div_in, dataset):
        if len(div_in.orderedContent()) == 0:
            return None

        try:
            begin, end = self.calculate_times(div_in, dataset)
        except TimeNegativeError:
            return None

        self.push_syncbase(dataset, begin)

        if begin is not None:
            begin = FullClockTimingType(begin)
        if end is not None:
            end = FullClockTimingType(end)

        new_elem = div_type(
            *self.convert_children(div_in, dataset),
            id=div_in.id,
            region=div_in.region,
            style=div_in.style,
            lang=div_in.lang,
            agent=div_in.agent,
            begin=begin,
            end=end
        )

        self.pop_syncbase(dataset)

        if len(new_elem.orderedContent()) == 0:
            new_elem = None

        return new_elem

    def convert_p(self, p_in, dataset):
        try:
            begin, end = self.calculate_times(p_in, dataset)
        except TimeNegativeError:
            return None

        self.push_syncbase(dataset, begin)

        if begin is not None:
            begin = FullClockTimingType(begin)
        if end is not None:
            end = FullClockTimingType(end)

        new_elem = p_type(
            *self.convert_children(p_in, dataset),
            id=p_in.id,
            space=p_in.space,
            lang=p_in.lang,
            region=p_in.region,
            style=p_in.style,
            begin=begin,
            end=end,
            agent=p_in.agent,
            role=p_in.role
        )

        self.pop_syncbase(dataset)

        if len(new_elem.orderedContent()) == 0:
            new_elem = None

        return new_elem

    def convert_span(self, span_in, dataset):
        try:
            begin, end = self.calculate_times(span_in, dataset)
        except TimeNegativeError:
            return None

        self.push_syncbase(dataset, begin)

        if begin is not None:
            begin = FullClockTimingType(begin)
        if end is not None:
            end = FullClockTimingType(end)

        new_elem = span_type(
            *self.convert_children(span_in, dataset),
            id=span_in.id,
            space=span_in.space,
            lang=span_in.lang,
            style=span_in.style,
            begin=begin,
            end=end,
            agent=span_in.agent,
            role=span_in.role
        )

        self.pop_syncbase(dataset)

        if len(new_elem.orderedContent()) == 0:
            new_elem = None

        return new_elem

    def convert_br(self, br_in, dataset):
        return br_type()

    def convert_unknown(self, element_in, dataset):
        new_elem = copy.deepcopy(element_in)
        return new_elem

    def convert_children(self, element, dataset):
        """
        Recursive step to convert child elements.

        :param element:
        :param dataset:
        :return:
        """
        output = []

        children = element.orderedContent()

        for item in children:
            if isinstance(item, NonElementContent):
                output.append(copy.deepcopy(item.value))
            elif isinstance(item, ElementContent):
                conv_elem = self.convert_element(item.value, dataset)
                if conv_elem is not None:
                    output.append(conv_elem)
            else:
                raise Exception('Can this even happen!??!?!?!')

        return output

    def convert_element(self, element, dataset):
        converter = self.map_type(element)
        return converter(element, dataset)

    def convert_document(self, root_element, dataset=None,
                         smpte_to_timedelta_converter=None):
        """
        Convert the EBU-TT-1 Document to an EBU-TT-3 document.

        :param root_element: The binding class for the EBU-TT-1 document's root element.
        :param dataset: An optional dataset for passing information into the conversion.
        :param smpte_to_timedelta_converter ISMPTEtoTimedeltaConverter: for mapping SMPTE to media timebase. Required if SMPTE timecodes are present.
        :return an EBU-TT-3 document's root tt element:
        """
        if dataset is None:
            self._semantic_dataset = {}
        else:
            self._semantic_dataset = dataset

        self._semantic_dataset['smpte_to_timebase_converter'] = \
            smpte_to_timedelta_converter

        # Make sure that any new elements we correct get the right bindings
        # Ideally we'd use EBUTT3Document.load_types_for_document() but that
        # causes a circular import loop, because EBUTT3Document imports
        # parts of bindings that include this (not sure why)
        load_types_for_document('ebutt3')
        converted_bindings = self.convert_element(
            root_element,
            self._semantic_dataset
        )

        return converted_bindings
