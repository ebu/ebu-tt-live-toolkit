from datetime import timedelta
from logging import getLogger
import copy
from pyxb.binding.basis import NonElementContent, ElementContent
from ebu_tt_live.bindings import tt
from ..bindings.validation.base import SemanticValidationMixin
from ..bindings.pyxb_utils import RecursiveOperation


log = logging.getLogger(__name__)


class EBUTT3Deduplicator(object):

    _style_id = None
    _style_attribute = None
    _sequence_identifier = None
    _sequence_number = None

    def __init__(self, style_id, style_attribute, sequence_identifier, sequence_number):
        if style_id is None or style_attribute is None:
            raise Exception()

        self._style_id = list(style_id)
        self._style_attribute = list(style_attribute)
        self._sequence_idtentifier = sequence_identifier
        self._sequence_number = sequence_number
        self._perform_deduplication()

    class ValidateAttribute(RecursiveOperation):

        _attribute_dataset = None

        def __init__(self, root_element):
            super(SemanticValidator, self).__init__(
                root_element=root_element,
                filter=self._attribute_validation_filter,
                children_iterator='_validatedChildren'
            )
            self._attribute_dataset = {}

        def _attribute_validation_filter(self, value, element):
            if isinstance(value, SemanticValidationMixin):
                return True
            else:
                return False

        def _before_element(self, value, element=None, parent_binding=None, **kwargs):
            value._semantic_before_traversal(dataset=self._attribute_dataset, element_content=element, parent_binding=parent_binding)
            pass

        def _process_element(self, value, element=None, parent_binding=None, **kwargs):
            return None

        def _after_element(self, value, element=None, parent_binding=None, **kwargs):
            value._semantic_after_traversal(dataset=self._attribute_dataset, element_content=element, parent_binding=parent_binding)

        def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
            return None

        def proceed(self, **kwargs):
            self._attribute_dataset = {}
            self._attribute_dataset.update(kwargs)
            super(SemanticValidator, self).proceed(**kwargs)
            return self._attrbute_dataset

    @property
    def _perform_deduplication(self):
