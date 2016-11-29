
from ..pyxb_utils import RecursiveOperation
from .base import SemanticValidationMixin
from pyxb.binding.basis import NonElementContent


class SemanticValidator(RecursiveOperation):

    _semantic_dataset = None

    def __init__(self, root_element):
        super(SemanticValidator, self).__init__(
            root_element=root_element,
            filter=self._semantic_validation_filter,
            children_iterator='_validatedChildren'
        )
        self._semantic_dataset = {}

    def _semantic_validation_filter(self, value, element):
        if isinstance(value, SemanticValidationMixin):
            return True
        else:
            return False

    def _before_element(self, value, element=None, parent_binding=None, **kwargs):
        value._semantic_before_traversal(dataset=self._semantic_dataset, element_content=element, parent_binding=parent_binding)
        pass

    def _process_element(self, value, element=None, parent_binding=None, **kwargs):
        return None

    def _after_element(self, value, element=None, parent_binding=None, **kwargs):
        value._semantic_after_traversal(dataset=self._semantic_dataset, element_content=element, parent_binding=parent_binding)

    def _process_non_element(self, value, non_element, parent_binding=None, **kwargs):
        return None

    def proceed(self, **kwargs):
        self._semantic_dataset = {}
        self._semantic_dataset.update(kwargs)
        super(SemanticValidator, self).proceed(**kwargs)
        return self._semantic_dataset
