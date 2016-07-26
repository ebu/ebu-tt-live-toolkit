"""
This file contains all the pyxb helpers needed for enabling a concise semantic validation approach.
"""

from pyxb import ValidationConfig, GlobalValidationConfig
from pyxb.binding.basis import _TypeBinding_mixin, simpleTypeDefinition, complexTypeDefinition, NonElementContent
from ebu_tt_live.strings import ERR_SEMANTIC_VALIDATION_TIMING_TYPE
from ebu_tt_live.errors import SemanticValidationError
import logging

log = logging.getLogger(__name__)


class SemanticValidationMixin(object):

    def _semantic_before_traversal(self, dataset, element_content=None):
        log.info(self)
        pass

    def _semantic_after_traversal(self, dataset, element_content=None):
        log.info(self)
        pass


class SemanticDocumentMixin(SemanticValidationMixin):

    # This dictionary exists to override attribute setters. Used in contextual parsing
    _attr_en = {}

    def _setAttribute(self, attr_en, value_lex):
        au = self.__class__.__bases__[1]._setAttribute(self, attr_en, value_lex)
        uri_tuple = attr_en.uriTuple()
        if uri_tuple in self._attr_en:
            self._attr_en[uri_tuple](self)
        return au

    def _semantic_before_validation(self):
        pass

    def _semantic_after_validation(self):
        """
        At this point the validation of syntax has passed and the semantic validation can now begin.
        A new traversal of the structure is needed to get the appropriate context down to individual parts of the nodes.
        """
        # Let's try to initiate DFS or BFS...
        semantic_dataset = {}
        pre_visited = set()
        post_visited = set()
        to_visit = []

        self._semantic_before_traversal(dataset=semantic_dataset)

        to_visit.extend(reversed(self._validatedChildren()))

        while to_visit:
            content = to_visit.pop()
            if content in post_visited or isinstance(content, NonElementContent):
                continue
            elif content in pre_visited:
                log.info('post visit step: {}'.format(content.value))
                content.value._semantic_after_traversal(dataset=semantic_dataset, element_content=content)
                post_visited.add(content)
            else:
                log.info('pre visit step: {}'.format(content.value))
                if isinstance(content.value, SemanticValidationMixin):  # WARNING: Refactoring naming changes
                    content.value._semantic_before_traversal(dataset=semantic_dataset, element_content=content)
                    pre_visited.add(content)
                    to_visit.append(content)

                if hasattr(content.value, '_validatedChildren'):
                    ordered_children = reversed(content.value._validatedChildren())
                    to_visit.extend(ordered_children)

        self._semantic_before_traversal(dataset=semantic_dataset)

    def _validateBinding_vx(self):
        # Step1: Before
        self._semantic_before_validation()

        # Step2: DFS
        # This line is hacky as f*** and non-standard way of getting the desired behaviour but python and MRO are not
        # always man's best friend...
        self.__class__.__bases__[1]._validateBinding_vx(self)

        # Step3: Process current object
        self._semantic_after_validation()


class TimeBaseValidationMixin(object):
    # The mixin approach is used since the inspected elements are all attributes of the element so they do not
    # take part in the traversal directly.

    def _semantic_timebase_validation(self, dataset, element_content):
        time_base = dataset['tt_element'].timeBase
        # Check typing of timing arguments against the timebase
        if hasattr(self, 'begin') and self.begin is not None and hasattr(self.begin, 'compatible_timebases'):
            timebases = self.begin.compatible_timebases()
            if time_base not in timebases['begin']:
                raise SemanticValidationError(
                    ERR_SEMANTIC_VALIDATION_TIMING_TYPE.format(
                        attr_type=type(self.begin),
                        attr_value=self.begin,
                        attr_name='begin',
                        time_base=time_base
                    )
                )
        if hasattr(self, 'dur') and self.dur is not None and hasattr(self.dur, 'compatible_timebases'):
            timebases = self.dur.compatible_timebases()
            if time_base not in timebases['dur']:
                raise SemanticValidationError(
                    ERR_SEMANTIC_VALIDATION_TIMING_TYPE.format(
                        attr_type=type(self.dur),
                        attr_value=self.dur,
                        attr_name='dur',
                        time_base=time_base
                    )
                )
        if hasattr(self, 'end') and self.end is not None and hasattr(self.end, 'compatible_timebases'):
            timebases = self.end.compatible_timebases()
            if time_base not in timebases['end']:
                raise SemanticValidationError(
                    ERR_SEMANTIC_VALIDATION_TIMING_TYPE.format(
                        attr_type=type(self.end),
                        attr_value=self.end,
                        attr_name='end',
                        time_base=time_base
                    )
                )

