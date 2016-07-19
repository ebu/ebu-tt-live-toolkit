"""
This file contains all the pyxb helpers needed for enabling a concise semantic validation approach.
"""

from pyxb import ValidationConfig, GlobalValidationConfig
from pyxb.binding.basis import _TypeBinding_mixin, simpleTypeDefinition, complexTypeDefinition, NonElementContent
import logging

log = logging.getLogger(__name__)


class SemanticValidationConfig(ValidationConfig):

    def __init__(self):
        log.warning('SemanticValidationConfig init {}'.format(hex(id(self))))

    def __del__(self):
        log.warning('SemanticValidationConfig deleted {}'.format(hex(id(self))))


class SemanticValidationMixin(object):

    _validationConfig_ = SemanticValidationConfig

    def _semantic_before_traversal(self, dataset):
        log.info(self)
        pass

    def _semantic_after_traversal(self, dataset):
        pass


class SemanticDocumentMixin(SemanticValidationMixin):

    def _semantic_before_validation(self):
        pass

    def _semantic_after_validation(self):
        """
        At this point the validation of syntax has passed and the semantic validation can now begin.
        A new traversal of the structure is needed to get the appropriate context down to individual parts of the nodes.
        """
        # Let's try to initiate DFS or BFS...
        semantic_dataset = {}
        visited = set()
        to_visit = []

        visited.add(self)

        self._semantic_before_traversal(dataset=semantic_dataset)

        to_visit.extend(reversed(self._validatedChildren()))

        log.info(to_visit)

        while to_visit:
            content = to_visit.pop()
            log.info('{} is {}'.format(content.value, isinstance(content, NonElementContent)))
            if isinstance(content, NonElementContent):
                continue
            if isinstance(content.value, SemanticValidationMixin):  # WARNING: Refactoring naming changes
                content.value._semantic_before_traversal(dataset=semantic_dataset)
                # WARNING: This should not be here TODO: move it
                content.value._semantic_after_traversal(dataset=semantic_dataset)
                visited.add(content)
            if hasattr(content.value, '_validatedChildren'):
                ordered_children = reversed(content.value._validatedChildren())
                filtered_children = [item for item in ordered_children if item not in visited]
                to_visit.extend(filtered_children)

    def _validateBinding_vx(self):
        # Step1: Before
        self._semantic_before_validation()

        # Step2: DFS
        # This line is hacky as f*** and non-standard way of getting the desired behaviour but python and MRO are not
        # always man's best friend...
        self.__class__.__bases__[1]._validateBinding_vx(self)

        # Step3: Process current object
        self._semantic_after_validation()
