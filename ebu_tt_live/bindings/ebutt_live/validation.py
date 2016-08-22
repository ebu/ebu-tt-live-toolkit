"""
This file contains all the pyxb helpers needed for enabling a concise semantic validation approach.
"""

from pyxb import ValidationConfig, GlobalValidationConfig
from pyxb.binding.basis import _TypeBinding_mixin, simpleTypeDefinition, complexTypeDefinition, NonElementContent
from ebu_tt_live.strings import ERR_SEMANTIC_VALIDATION_TIMING_TYPE, DOC_SEMANTIC_VALIDATION_SUCCESSFUL, \
    DOC_SYNTACTIC_VALIDATION_SUCCESSFUL
from ebu_tt_live.errors import SemanticValidationError, LogicError
from .pyxb_utils import get_xml_parsing_context
from datetime import timedelta
import logging

log = logging.getLogger(__name__)
document_logger = logging.getLogger('document_logger')


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
        document_logger.info(DOC_SYNTACTIC_VALIDATION_SUCCESSFUL)
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
        document_logger.info(DOC_SEMANTIC_VALIDATION_SUCCESSFUL)
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


class TimingValidationMixin(object):
    """
    This mixin is meant to be applied to timed elements (body, div, p, span) and provides parser hooks for timing
    attributes as well as a generic semantic validation for timing attributes in the document's timeBase.
    """

    _computed_begin_time = None
    _computed_end_time = None

    @property
    def computed_begin_time(self):
        return self._computed_begin_time

    @property
    def computed_end_time(self):
        return self._computed_end_time

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

    def _pre_init_variables(self, dataset, element_content):
        self._begin_timedelta = self.begin and self.begin.timedelta or None
        self._end_timedelta = self.end and self.end.timedelta or None
        # We make sure end time is always none at the beginning because it can cause a LogicError with a stale value
        self._computed_begin_time = None
        self._computed_end_time = None
        self._semantic_dataset = dataset

    def _post_cleanup_variables(self):
        del self._semantic_dataset
        del self._begin_timedelta
        del self._end_timedelta

    def _pre_assign_end(self, proposed_end):
        self._semantic_dataset['timing_end_stack'].append(proposed_end)
        self._semantic_dataset['timing_end_limit'] = max(self._semantic_dataset.get('timing_end_limt', timedelta()), proposed_end)
        self._computed_end_time = proposed_end

    def _pre_calculate_end(self):

        if self._end_timedelta is not None:
            if self._semantic_dataset['timing_end_stack']:
                # If there was already an end time in some parent element.
                proposed_end = min(self._semantic_dataset['timing_syncbase'] + self._end_timedelta, self._semantic_dataset['timing_end_stack'][-1])
            # New end
            else:
                proposed_end = self._semantic_dataset['timing_syncbase'] + self._end_timedelta
            # If we have it assign it
            self._pre_assign_end(proposed_end)

    def _pre_assign_begin(self, proposed_begin):
        if proposed_begin is not None:
            # Store the element's activation begin times
            # Let's push it onto the stack.
            self._semantic_dataset['timing_begin_stack'].append(proposed_begin)
            self._semantic_dataset['timing_syncbase'] += proposed_begin

        # If we have a non-zero availability time we need to factor it in BUT the syncbase stays
        if self._semantic_dataset['availability_time']:
            self._computed_begin_time = max(self._semantic_dataset['timing_syncbase'],
                                            self._semantic_dataset['availability_time'])
        else:
            self._computed_begin_time = self._semantic_dataset['timing_syncbase']

    def _pre_calculate_begin(self):
        self._pre_assign_begin(self._begin_timedelta)

        if self._computed_begin_time is not None and self._begin_timedelta is not None:
            # This will help us find the earliest descendant element of body
            if self._semantic_dataset['timing_begin_limit'] is not None \
                    and self._semantic_dataset['timing_begin_limit'] > self._computed_begin_time \
                    or self._semantic_dataset['timing_begin_limit'] is None:
                # This means that timing begin limit needs updating
                self._semantic_dataset['timing_begin_limit'] = self._computed_begin_time

    def _semantic_preprocess_timing(self, dataset, element_content):
        """
        As the validator traverses in a Depth First Search this is the hook function to call on the way DOWN.

        Steps to take:
          - Initialize temporary variables
          - Calculate end timing if element defines an end time
          - Calculate begin time and syncbase for children

        :param dataset: Semantic dataset from semantic validation framework
        :param element_content: PyXB's binding placeholder for this binding instance
        """

        self._pre_init_variables(dataset, element_content)

        self._pre_calculate_end()

        # These assignments must happen last otherwise the syncbase will be wrong
        # in calculations happening after syncbase adjustment.
        self._pre_calculate_begin()

    def _post_pop_begin(self):
        if self._begin_timedelta is not None:
            # We pushed on the stack it is time to pop it. It could probably be removed
            # and replaced with self._begin_timedelta
            begin_timedelta = self._semantic_dataset['timing_begin_stack'].pop()
            self._semantic_dataset['timing_syncbase'] -= begin_timedelta

    def _post_pop_end(self):
        end_timedelta = None

        if self._end_timedelta is not None:
            # We pushed on the stack it is time to pop it
            end_timedelta = self._semantic_dataset['timing_end_stack'].pop()

        return end_timedelta

    def _semantic_postprocess_timing(self, dataset, element_content):
        """
        As the validator traverses in a Depth First Search this is the hook function to call on the way UP

        Steps to take:
          - Fill in end times if element doesn't define end time
          - Try using information from its children
          - if no children are found look at parents end time constraints.

        :param dataset: Semantic dataset from semantic validation framework
        :param element_content: PyXB's binding placeholder for this binding instance
        """

        self._post_pop_begin()
        # This end timedelta is an absolute calculated value on the timeline. Not relative.
        end_timedelta = self._post_pop_end()

        # If the forward running part of the traversal could not assign an end time we can use the backwards route
        # which is in a way similar to dynamic programming because we take the children computed times and take the
        # maximum value from them. SPECIAL case: a single leaf element with an undefined end time renders the entire
        # branch undefined

        if end_timedelta is not None and self.computed_end_time is None \
                or end_timedelta is None and self.computed_end_time is not None:
            # This is just a simple sanity check. It should never be triggered.
            # Should the calculation be changed this filters out an obvious source of error.
            raise LogicError()

        if self.computed_end_time is None:
            # This requires calculation based on the timings in its children.

            # All timing containers are complexTypes so we can call orderedContent safely
            children = filter(lambda item: isinstance(item, TimingValidationMixin), [x.value for x in self.orderedContent()])
            # Order of statements is important
            if not children:
                # This means we are in a timing container leaf.
                if not self._semantic_dataset['timing_end_stack']:
                    # Here we go an endless document. Pointless but for clarity's sake assign it explicitly to None.
                    self._computed_end_time = None
                else:
                    # Try to assign it the last specified ancestor
                    self._computed_end_time = self._semantic_dataset['timing_end_stack'][-1]
            else:
                children_computed_end_times = [item.computed_end_time for item in children]

                if None in children_computed_end_times:
                    # The endless document case propagates up
                    self._computed_end_time = None
                else:
                    # Propagate the longest end time among the children
                    self._computed_end_time = max(children_computed_end_times)

    # The mixin approach is used since there are multiple timed elements types.
    # The inspected elements are all attributes of the element so they do not
    # take part in the traversal directly we process them in the timed element's context instead: body, div, p, span
    def _semantic_timebase_validation(self, dataset, element_content):
        time_base = dataset['tt_element'].timeBase
        if self.begin is not None:
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
        if self.end is not None:
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


class BodyTimingValidationMixin(TimingValidationMixin):
    """
    The body element seems to be exception from too many rules and makes one common validator pretty difficult
    to manage. This subclass is meant to call all the extensions/limitations for the body element that does not apply
    to timed containers in general in the EBU-TT-Live spec.
    """

    def _pre_init_variables(self, dataset, element_content):
        super(BodyTimingValidationMixin, self)._pre_init_variables(dataset, element_content)
        self._dur_timedelta = self.dur and self.dur.timedelta or None

    def _post_cleanup_variables(self):
        del self._dur_timedelta
        super(BodyTimingValidationMixin, self)._post_cleanup_variables()

    def _pre_calculate_end(self):
        # This is all for the body element because of the dur attribute
        if self._dur_timedelta is not None:
            if self._begin_timedelta is not None and self._end_timedelta is not None:
                # This is a special (stupid) edge case..:
                proposed_end = min(self._dur_timedelta + self._begin_timedelta, self._end_timedelta)
            elif self._begin_timedelta is not None and self._end_timedelta is None:
                proposed_end = self._dur_timedelta + self._begin_timedelta
            elif self._begin_timedelta is None and self._end_timedelta is None:
                # In this case the document end at availability time + dur
                proposed_end = self._semantic_dataset['availability_time'] + self._dur_timedelta
            elif self._begin_timedelta is None and self._end_timedelta is not None:
                proposed_end = min(self._semantic_dataset['availability_time'] + self._dur_timedelta, self._end_timedelta)
        else:
            # Fallback case if there is no duration specified the same as the other containers
            super(BodyTimingValidationMixin, self)._pre_calculate_end()
            # WARNING this assigns it so we are done
            return
        # If one of our special ifs worked let's assign the value here.
        self._pre_assign_end(proposed_end)

    def _pre_calculate_begin(self):
        self._pre_assign_begin(self._begin_timedelta)

    def _post_pop_end(self):
        end_timedelta = None

        if self._end_timedelta is not None or self._dur_timedelta is not None:
            # We pushed on the stack it is time to pop it
            end_timedelta = self._semantic_dataset['timing_end_stack'].pop()

        return end_timedelta

    def _semantic_timebase_validation(self, dataset, element_content):

        super(BodyTimingValidationMixin, self)._semantic_timebase_validation(dataset, element_content)
        time_base = dataset['tt_element'].timeBase

        if self.dur is not None:
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
