
from datetime import timedelta
import logging
import copy
from ebu_tt_live.bindings.validation.base import SemanticValidationMixin, IDMixin
from ebu_tt_live.bindings.pyxb_utils import RecursiveOperation
from ebu_tt_live.bindings.validation.presentation import StyledElementMixin
from ebu_tt_live.bindings import style_type, region_type
from ebu_tt_live.errors import DiscardElement
from ebu_tt_live.bindings import ebuttdt

# Splicer and segmentation
# ========================

log = logging.getLogger(__name__)


class EBUTT3Segmenter(RecursiveOperation):

    _begin = None
    _end = None
    _document = None
    _segment = None
    _deconflict_ids = None
    _instance_mapping = None
    _semantic_dataset = None

    def __init__(self, document, begin=None, end=None, deconflict_ids=False):
        super(EBUTT3Segmenter, self).__init__(
            root_element=document.binding
        )
        self._document = document
        log.debug('Segmenter created')
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

        # Map instances to their converted versions because not everything has an id and there is no complete
        # equivalence check either
        dataset['instance_mapping'][element] = celem

        return celem

    def _before_element(self, value, element=None, parent_binding=None, **kwargs):
        if isinstance(value, SemanticValidationMixin):  # WARNING: Refactoring naming changes
            value._semantic_before_copy(dataset=self._semantic_dataset, element_content=element)

    def _process_element(self, value, element=None, parent_binding=None, **kwargs):
        if isinstance(value, SemanticValidationMixin):  # WARNING: Refactoring naming changes
            # Shallow copy element
            celem = self._do_copy(value, dataset=self._semantic_dataset)
            # Call preprocess hooks of current element's subtree
            value._semantic_before_subtree_copy(
                copied_instance=celem,
                dataset=self._semantic_dataset,
                element_content=element
            )
        else:
            self._do_copy(value, dataset=self._semantic_dataset)

    def _after_element(self, value, element=None, parent_binding=None, **kwargs):
        if isinstance(value, SemanticValidationMixin):
            # Call postprocess hooks of current element
            celem = self._semantic_dataset['instance_mapping'][value]
            try:
                value._semantic_after_subtree_copy(
                    copied_instance=celem,
                    dataset=self._semantic_dataset,
                    element_content=element
                )

                if element:
                    value._do_link_copy_with_copied_parent(
                        dataset=self._semantic_dataset,
                        element_content=element,
                        parent_binding=parent_binding
                    )
                else:
                    self._segment = celem
            except DiscardElement:
                log.debug('{} discarded during copy'.format(value))


    def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
        parent = self._semantic_dataset['instance_mapping'][parent_binding]
        parent.append(copy.deepcopy(value))

    def proceed(self, **kwargs):
        self._semantic_dataset = {}
        self._semantic_dataset.update(kwargs)

        super(EBUTT3Segmenter, self).proceed(**kwargs)

    def _convert_time(self, timedelta_value):
        if self.document.time_base == 'clock':
            return ebuttdt.LimitedClockTimingType(timedelta_value)
        elif self.document.time_base == 'media':
            return ebuttdt.FullClockTimingType(timedelta_value)
        else:
            return ebuttdt.SMPTETimingType(timedelta_value)

    def _prune_orphan_elements(self):
        """
        Unused elements need to go from the head section.
        :return:
        """
        # TODO: This is not too nice. No time now, improve later.
        for item in self._semantic_dataset['orphaned_elements']:
            if isinstance(item, style_type):
                self._segment.head.styling.style.remove(self._semantic_dataset['instance_mapping'][item])
            if isinstance(item, region_type):
                self._segment.head.layout.region.remove(self._semantic_dataset['instance_mapping'][item])

        if len(self._segment.head.styling.style) == 0:
            self._segment.head.styling = None
        if len(self._segment.head.layout.region) == 0:
            self._segment.head.layout.region = None

    def compute_document_segment(self):
        # Init
        # Make sure it is validated
        self.document.validate()
        # Get the p and span elements in the range from the timeline
        affected_elements = self.document.lookup_range_on_timeline(begin=self.begin, end=self.end)

        affected_elements = set(affected_elements)

        # Empty document edge-case: Body is always affected
        affected_elements.add(self.document.binding.body)
        orphaned_elements = set()

        for item in [
            elem for elem in affected_elements
            if isinstance(elem, StyledElementMixin)
        ]:
            # Styles and regions are meant to be preserved. We put in everything that is likely to be needed
            # NOTE: There is a possibility that after copying some containers stay empty so they get removed from the
            # copy . In that case the unreferenced elements will be removed from the head.
            affected_elements.update(item.validated_styles)
            orphaned_elements.update(item.validated_styles)
            if item.inherited_region is not None:
                affected_elements.add(item.inherited_region)
                orphaned_elements.add(item.inherited_region)

        dataset = {
            'segment_begin': self.begin,
            'segment_end': self.end,
            'affected_elements': affected_elements,
            'orphaned_elements': orphaned_elements,
            'instance_mapping': {},
            'capture_counter': 0,
            'tt_element': self.document.binding
        }

        self.proceed(**dataset)

        # Remove orphaned content
        self._prune_orphan_elements()

        # Drop instance_mapping
        self._instance_mapping = dataset.pop('instance_mapping')

        # Empty document edge-case
        if len(self._segment.body.orderedContent()) == 0:
            self._segment.body.begin = self._convert_time(self.begin)
            self._segment.body.end = self._convert_time(self.end)
