
from datetime import timedelta
import logging
import copy
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings.validation import SemanticValidationMixin, StyledElementMixin, IDMixin

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
            element.deconflict_id()


    def _do_copy(self, element, dataset):
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

        to_visit.extend(list(self._document.binding.orderedContent()))

        while to_visit:
            content = to_visit.pop()

            if content in post_visited or isinstance(content, NonElementContent):
                # This means we visited the current element already.
                continue
            elif content in pre_visited:
                # This means we visited the current element's preprocessing and now postprocessing is in order
                log.debug('post copy step: {}'.format(content.value))
                # Call postprocess hooks of current element
                content.value._semantic_after_subtree_copy(dataset=dataset, element_content=content)
                if content.value not in dataset['affected_elements']:
                    pass
                post_visited.add(content)
            else:
                # This means the current element has not been processed yet. Preprocessing is in order.
                log.debug('pre copy step: {}'.format(content.value))
                if isinstance(content.value, SemanticValidationMixin):  # WARNING: Refactoring naming changes
                    # Shallow copy element
                    self._do_copy(content.value, dataset=dataset)
                    # Call preprocess hooks of current element
                    content.value._semantic_before_subtree_copy(dataset=dataset, element_content=content)
                    pre_visited.add(content)
                    to_visit.append(content)

                if hasattr(content.value, 'orderedContent'):
                    to_visit.extend(list(content.value.orderedContent()))

        self._segment = segment

    def compute_document_segment(self):
        # Init
        # Make sure it is validated
        self.document.validate()
        # Get the p and span elements in the range from the timeline
        affected_elements = self.document.lookup_range_on_timeline(begin=self.begin, end=self.end)

        for item in [elem for elem in affected_elements if isinstance(elem, StyledElementMixin)]:
            # Styles and regions are meant to be preserved
            affected_elements.extend(item.validated_styles)
            if item.inherited_region is not None:
                affected_elements.append(item.inherited_region)

        dataset = {
            'affected_elements': affected_elements,
            'instance_mapping': {},
            'capture_counter': 0,
            'tt_element': self.document.binding
        }

        self.iterate_through_document(dataset=dataset)

        # Map instances to their converted versions because not everything has an id and there is no complete
        # equivalence check either
        self._instance_mapping = dataset.pop('instance_mapping')


