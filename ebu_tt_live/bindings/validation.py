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

    def _semantic_after_validation(self, **extra_kwargs):
        """
        After PyXB successfully validated the syntax this hook runs where the user may execute custom code.

        At this point the validation of syntax has passed and the semantic validation can now begin.
        A new traversal of the structure is needed to get the appropriate context down to individual parts of the nodes.
        """
        # Let's initiate DFS

        # Create new semantic context object
        semantic_dataset = {}
        semantic_dataset.update(extra_kwargs)
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

        return semantic_dataset

    def _validateBinding_vx(self, **extra_kwargs):
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
        semantic_dataset = self._semantic_after_validation(**extra_kwargs)

        return semantic_dataset

    def validateBinding (self, **extra_kwargs):
        """Check whether the binding content matches its content model.

        @return: C{True} if validation was not performed due to settings.
        @return: Complex result dictionary with success and semantic_dataset keys.
        @raise pyxb.BatchContentValidationError: complex content does not match model # Wondering about this...
        @raise pyxb.SimpleTypeValueError: attribute or simple content fails to satisfy constraints
        """
        if self._performValidation():
            result = self._validateBinding_vx(**extra_kwargs)
            return {
                "success": True,
                "semantic_dataset": result
            }
        return True


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

    def _semantic_preprocess_timing(self, dataset, element_content):
        if hasattr(self, 'begin') and self.begin is not None:
            # Let's push it onto the stack
            begin_timedelta = self.begin.timedelta
            if not dataset['timing_begin_stack']:
                # This means we are at a first timing container
                print 'new firt timecontainer detected'
                if dataset['timing_resolved_begin'] is None or dataset['timing_resolved_begin'] < begin_timedelta:
                    print 'adding timing_resolved_begin {}'.format(begin_timedelta)
                    dataset['timing_resolved_begin'] = begin_timedelta
            dataset['timing_begin_stack'].append(begin_timedelta)
            dataset['timing_accum_begin'] += begin_timedelta

        if hasattr(self, 'dur') and self.dur is not None:
            # if self.begin is None:
            #     raise NotImplementedError('Availability time needed to process timing')
            pass

        if hasattr(self, 'end') and self.end is not None:
            # Let's push it onto the stack
            dataset['timing_end_stack'].append(self.end)

    def _semantic_postprocess_timing(self, dataset, element_content):
        if hasattr(self, 'begin') and self.begin is not None:
            # We pushed on the stack it is time to pop it
            dataset['timing_begin_stack'].pop()

        if hasattr(self, 'end') and self.end is not None:
            # We pushed on the stack it is time to pop it
            dataset['timing_end_stack'].pop()

    # The mixin approach is used since there are multiple timed elements types.
    # The inspected elements are all attributes of the element so they do not
    # take part in the traversal directly we process them in the timed element's context instead: body, div, p, span
    def _semantic_timebase_validation(self, dataset, element_content):
        time_base = dataset['tt_element'].timeBase
        if hasattr(self, 'begin') and self.begin is not None:
            if hasattr(self.begin, 'compatible_timebases'):
                # Check typing of begin attribute against the timebase
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
        if hasattr(self, 'dur') and self.dur is not None:
            if hasattr(self.dur, 'compatible_timebases'):
                # Check typing of dur attribute against the timebase
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
        if hasattr(self, 'end') and self.end is not None:
            if hasattr(self.end, 'compatible_timebases'):
                # Check typing of end attribute against the timebase
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
