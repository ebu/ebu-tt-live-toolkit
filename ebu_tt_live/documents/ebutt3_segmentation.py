
from datetime import timedelta
import logging
import copy
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings.validation import SemanticValidationMixin, StyledElementMixin, IDMixin
from ebu_tt_live.bindings import tt
from ebu_tt_live.errors import OutsideSegmentError

# Splicer and segmentation
# ========================

log = logging.getLogger(__name__)


class EBUTT3Segmenter(object):

    _begin = None
    _end = None
    _document = None
    _segment = None
    _deconflict_ids = None
    _instance_mapping = None

    def __init__(self, document, begin=None, end=None, deconflict_ids=False):
        self._document = document
        log.info('Segmenter created')
        if begin is not None:
            assert isinstance(begin, timedelta)
            self._begin = begin
        if end is not None:
            assert isinstance(end, timedelta)
            self._end = end

        self._deconflict_ids = deconflict_ids

        self.compute_document_segment()

    @property
    def begin(self):
        return self._begin

    @property
    def end(self):
        return self._end

    @property
    def document(self):
        return self._document

    @property
    def segment(self):
        return self._segment

    @property
    def deconflict_ids(self):
        return self._deconflict_ids

    def _do_deconflict_id(self, element):
        if isinstance(element, IDMixin):
            element.deconflict_id(self._document.sequence_number)

    def _do_copy(self, element, dataset):

        if hasattr(element, '_semantic_copy'):
            celem = element._semantic_copy(dataset=dataset)
        else:
            celem = copy.copy(element)

        if self.deconflict_ids:
            self._do_deconflict_id(celem)

        dataset['instance_mapping'][element] = celem

        return celem

    def iterate_through_document(self, dataset):
        # Collections of visited elements
        pre_visited = set()
        post_visited = set()
        to_visit = []

        segment = self._do_copy(element=self.document.binding, dataset=dataset)

        ordered_content = list(reversed(list(self._document.binding.orderedContent())))
        log.debug(ordered_content)
        to_visit.extend(ordered_content)
        log.debug(to_visit)

        while to_visit:
            content = to_visit.pop()

            if content in post_visited:
                # This means we visited the current element already.
                continue
            elif content in pre_visited:
                # This means we visited the current element's preprocessing and now postprocessing is in order
                log.debug('post copy step: {}'.format(content.value))
                if isinstance(content.value, SemanticValidationMixin):
                    # Call postprocess hooks of current element
                    celem = dataset['instance_mapping'][content.value]
                    content.value._semantic_after_subtree_copy(
                        copied_instance=celem,
                        dataset=dataset,
                        element_content=content
                    )
                    content.value._do_link_with_parent(dataset=dataset, element_content=content)
                elif isinstance(content, NonElementContent):
                    parent = dataset['instance_mapping'][content.parent_binding]
                    parent.append(copy.deepcopy(content.value))
                    content.parent_binding = None

                post_visited.add(content)
            else:
                # This means the current element has not been processed yet. Preprocessing is in order.
                log.debug('pre copy step: {}'.format(content.value))
                if isinstance(content, ElementContent):
                    if isinstance(content.value, SemanticValidationMixin):  # WARNING: Refactoring naming changes
                        # Shallow copy element
                        try:
                            # Call preprocess hooks of current element
                            content.value._semantic_before_copy(dataset=dataset, element_content=content)
                        except OutsideSegmentError:
                            # Yay we don't need to process further
                            continue
                        # Shallow copy element
                        celem = self._do_copy(content.value, dataset=dataset)
                        # Call preprocess hooks of current element's subtree
                        content.value._semantic_before_subtree_copy(
                            copied_instance=celem,
                            dataset=dataset,
                            element_content=content
                        )
                    else:
                        self._do_copy(content.value, dataset=dataset)

                # In case of NonElementContent we do not need to copy just yet

                pre_visited.add(content)
                to_visit.append(content)

                if hasattr(content.value, 'orderedContent'):
                    to_visit.extend(list(reversed(list(content.value.orderedContent()))))

        segment._setElement(tt)

        self._segment = segment

    def compute_document_segment(self):
        # Init
        # Make sure it is validated
        self.document.validate()
        # Get the p and span elements in the range from the timeline
        affected_elements = self.document.lookup_range_on_timeline(begin=self.begin, end=self.end)

        affected_elements = set(affected_elements)

        for item in [elem for elem in affected_elements if isinstance(elem, StyledElementMixin)]:
            # Styles and regions are meant to be preserved
            affected_elements.update(item.validated_styles)
            if item.inherited_region is not None:
                affected_elements.add(item.inherited_region)

        dataset = {
            'segment_begin': self.begin,
            'segment_end': self.end,
            'affected_elements': affected_elements,
            'instance_mapping': {},
            'capture_counter': 0,
            'tt_element': self.document.binding
        }

        self.iterate_through_document(dataset=dataset)

        # Map instances to their converted versions because not everything has an id and there is no complete
        # equivalence check either
        self._instance_mapping = dataset.pop('instance_mapping')
