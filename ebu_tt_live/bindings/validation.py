"""
This file contains all the pyxb helpers needed for enabling a concise semantic validation approach.
"""

from pyxb import ValidationConfig, GlobalValidationConfig
from pyxb.binding.basis import _TypeBinding_mixin, simpleTypeDefinition, complexTypeDefinition, NonElementContent
from ebu_tt_live.strings import ERR_SEMANTIC_VALIDATION_TIMING_TYPE
from ebu_tt_live.errors import SemanticValidationError
from .pyxb_utils import get_xml_parsing_context
import logging

log = logging.getLogger(__name__)


class SemanticValidationMixin(object):
    """
    This mixin contains the necessary boilerplate to enable semantic validation as well as enabling _setAttribute hooks
    to help populate the context object with useful data.
    """

    # This dictionary exists to override attribute setters. Used in contextual parsing
    _attr_en_pre = {}
    _attr_en_post = {}

    def _setAttribute(self, attr_en, value_lex):
        uri_tuple = attr_en.uriTuple()
        if uri_tuple in self._attr_en_pre:
            self._attr_en_pre[uri_tuple](self, attr_en, value_lex)
        au = super(SemanticValidationMixin, self)._setAttribute(attr_en, value_lex)
        if uri_tuple in self._attr_en_post:
            self._attr_en_post[uri_tuple](self, au)
        return au

    def _semantic_before_traversal(self, dataset, element_content=None):
        """
        Semantic validation preprocess hook.
        :param dataset: semantic context object
        :param element_content: the element itself
        """
        pass

    def _semantic_after_traversal(self, dataset, element_content=None):
        """
        Semantic validation postprocess hook.
        :param dataset: semantic context object
        :param element_content: the element itself
        """
        pass

    def _semantic_attributes_missing(self, attr_names):
        """
        Making sure that attributes specified in attr_names have no value defined on the binding.
        :param attr_names: The attributes that were defined on the element.
        :return:
        """
        result = [attr for attr in attr_names if getattr(self, attr) is None]
        return result

    def _semantic_attributes_present(self, attr_names):
        """
        Making sure that attributes specified in attr_names have a value defined on the binding
        :param attr_names: The missing attributes that were not defined.
        :return:
        """
        result = [attr for attr in attr_names if getattr(self, attr) is not None]
        return result



class SemanticDocumentMixin(SemanticValidationMixin):

    def _semantic_before_validation(self):
        """
        Before PyXB starts its syntactic validation this hook runs where the user may execute custom code.
        """
        pass

    def _semantic_after_validation(self):
        """
        After PyXB successfully validated the syntax this hook runs where the user may execute custom code.

        At this point the validation of syntax has passed and the semantic validation can now begin.
        A new traversal of the structure is needed to get the appropriate context down to individual parts of the nodes.
        """
        # Let's initiate DFS

        # Create new semantic context object
        semantic_dataset = {}
        # Collections of visited elements
        pre_visited = set()
        post_visited = set()
        to_visit = []

        # Call preprocess hooks for tt element
        self._semantic_before_traversal(dataset=semantic_dataset)

        to_visit.extend(reversed(self._validatedChildren()))

        while to_visit:
            content = to_visit.pop()
            if content in post_visited or isinstance(content, NonElementContent):
                # This means we visited the current element already.
                continue
            elif content in pre_visited:
                # This means we visited the current element's preprocessing and now postprocessing is in order
                log.debug('post visit step: {}'.format(content.value))
                # Call postprocess hooks of current element
                content.value._semantic_after_traversal(dataset=semantic_dataset, element_content=content)
                post_visited.add(content)
            else:
                # This means the current element has not been processed yet. Preprocessing is in order.
                log.debug('pre visit step: {}'.format(content.value))
                if isinstance(content.value, SemanticValidationMixin):  # WARNING: Refactoring naming changes
                    # Call preprocess hooks of current element
                    content.value._semantic_before_traversal(dataset=semantic_dataset, element_content=content)
                    pre_visited.add(content)
                    to_visit.append(content)

                if hasattr(content.value, '_validatedChildren'):
                    ordered_children = reversed(content.value._validatedChildren())
                    to_visit.extend(ordered_children)

        # Call postprocess hooks for tt element
        self._semantic_after_traversal(dataset=semantic_dataset)

    def _validateBinding_vx(self):
        """
        At this point we can hook into PyXB's validation flow and call our hooks:
        _semantic_before_validation() and _semantic_after_validation()
        """
        # Step1: Before
        self._semantic_before_validation()

        # Step2: DFS
        # This line is hacky as f*** and non-standard way of getting the desired behaviour but python and MRO are not
        # always man's best friend...
        self.__class__.__bases__[1]._validateBinding_vx(self)

        # Step3: Process current object
        self._semantic_after_validation()


class TimeBaseValidationMixin(object):
    """
    This mixin is meant to be applied to timed elements (body, div, p, span) and provides parser hooks for timing
    attributes as well as a generic semantic validation for timing attributes in the document's timeBase.
    """

    def _pre_timing_set_attribute(self, attr_en, attr_use):
        # Pass in the timing_attribute_name to the context to help the timing type constructor refuse creation
        context = get_xml_parsing_context()
        if context is not None:
            # This means we are in XML parsing mode
            context['timing_attribute_name'] = attr_en.localName()

    def _post_timing_set_attribute(self, attr_use):
        context = get_xml_parsing_context()
        if context is not None:
            # Clean up after successful creation
            context.pop('timing_attribute_name', None)


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
