from datetime import timedelta

from ebu_tt_live.bindings import get_xml_parsing_context
from ebu_tt_live.errors import LogicError, SemanticValidationError, OutsideSegmentError, OverlappingActiveElementsError
from ebu_tt_live.strings import ERR_SEMANTIC_VALIDATION_TIMING_TYPE
import itertools

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

    def _element_badly_timed(self, value, element):
        return (element.begin is not None and \
                element.end is not None and \
                element.end <= element.begin)
        
    def _post_cleanup_variables(self):
        del self._semantic_dataset
        del self._begin_timedelta
        del self._end_timedelta

    def _pre_assign_end(self, proposed_end):
        self._semantic_dataset['timing_end_stack'].append(proposed_end)
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
        # this checks if it is a ttd doc
        if 'ttd_element' in self._semantic_dataset:
            self._computed_begin_time = self._semantic_dataset['timing_syncbase']
        else:
            #assuming that this is a live document
            if self._semantic_dataset['availability_time']:
                self._computed_begin_time = max(self._semantic_dataset['timing_syncbase'],
                                                self._semantic_dataset['availability_time'])
            else:
                self._computed_begin_time = self._semantic_dataset['timing_syncbase']

    def _pre_calculate_begin(self):
        self._pre_assign_begin(self._begin_timedelta)

    def _post_calculate_begin(self, children):
        """
        The computed begin time shall be moved down to match that of the earliest child begin time in case the container
        does not specify a begin time itself. NOTE: This does not modify the syncbase.

        :param children:
        :return:
        """

        if not children:
            return

        children_computed_begin_times = [item.computed_begin_time for item in children]

        earliest_child_computed_begin = min(children_computed_begin_times)
        if earliest_child_computed_begin > self._computed_begin_time:
            # Adjustment scenario
            # If no parent element specified a begin time, then we have found
            # a case for the "earliest specified computed begin time" as per the
            # specification and we can adjust the begin time to match the
            # children's begin time.
            if len(self._semantic_dataset['timing_begin_stack']) == 0:
                self._computed_begin_time = earliest_child_computed_begin

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
        begin_timedelta = None

        if self._begin_timedelta is not None:
            # We pushed on the stack it is time to pop it. It could probably be removed
            # and replaced with self._begin_timedelta
            begin_timedelta = self._semantic_dataset['timing_begin_stack'].pop()
            self._semantic_dataset['timing_syncbase'] -= begin_timedelta

        return begin_timedelta

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
          - Try using computed_end_time information from its children
          - If no children are found look at parents end time constraints.
          - Finalize computed_begin_time if begin is not specified using computed_begin_time of children.

        :param dataset: Semantic dataset from semantic validation framework
        :param element_content: PyXB's binding placeholder for this binding instance
        """

        begin_timedelta = self._post_pop_begin()
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

        children = None

        if self.computed_end_time is None:
            # This requires calculation based on the timings in its children.

            # All timing containers are complexTypes so we can call orderedContent safely
            # but we don't want to bother with explicitly badly timed elements so filter
            # them out.
            children = [item for item in [x.value for x in self.orderedContent()] if isinstance(item, TimingValidationMixin) \
                              and not item._element_badly_timed(value=None, element=item)]
                              
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

        # When we are the body element we need to check that our explicit timings
        # are valid, i.e. deal with end before befin by discarding this element 
        # from computed time calculation as per spec requirement. Since we exclude all
        # elements where this is the case using the _element_badly_timed
        # function as a filter, this only applies to the body element (on which
        # the filter function doesn't get called).
        if isinstance(self, BodyTimingValidationMixin) \
            and self._element_badly_timed(value=None, element=self):
            self._computed_end_time = None
            self._computed_begin_time = timedelta(0)

        if begin_timedelta is None:

            if children is None:
                children = [item for item in [x.value for x in self.orderedContent()] if isinstance(item, TimingValidationMixin) \
                                  and not item._element_badly_timed(value=None, element=item)]

            self._post_calculate_begin(children=children)

        self._post_cleanup_variables()

    # The mixin approach is used since there are multiple timed element types.
    # The inspected values are all attributes of the element so they do not
    # take part in the traversal directly we process them in the timed element's context instead: body, div, p, span
    def _semantic_timebase_validation(self, dataset, element_content):
        if 'tt_element' in dataset:
            time_base = dataset['tt_element'].timeBase
        else:
            time_base = dataset['ttd_element'].timeBase
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

    def _semantic_manage_timeline(self, dataset, element_content):
        # Get the document instance
        doc = dataset['document']

        # Register on timeline
        doc.add_to_timeline(self)


    # This section covers the copying operations of timed containers.

    # this semantic validation only applies on ebu-tt-d type elements where the the origin and extent units are in %
    def _semantic_validate_active_areas(self, dataset):
        # Get the document instance
        doc = dataset['document']
        if self.computed_begin_time is not None and self.computed_end_time is not None:
            affected_elements = doc.lookup_range_on_timeline(self.computed_begin_time, self.computed_end_time)
            if len(affected_elements) > 1:
                for elem1, elem2 in itertools.combinations(affected_elements, 2):
                  if elem1 != elem2:
                    if elem1.region is not None and elem2.region is not None \
                        and elem1.region != elem2.region: #checking if the elements have regions
                        # Getting coordinates from the attribute eg ['14% 16%']
                        elem1_region = dataset['elements_by_id'][elem1.region]
                        elem2_region = dataset['elements_by_id'][elem2.region]
                        origins_1 = elem1_region.origin.split(' ')
                        origins_2 = elem2_region.origin.split(' ')
                        l1 =  [float(origin.strip('%')) for origin in origins_1] 
                        l2 =  [float(origin.strip('%')) for origin in origins_2] 
                        extents_1 = elem1_region.extent.split(' ')
                        extents_2 = elem1_region.extent.split(' ')
                        r1 = [float(extent.strip('%')) for extent in extents_1] 
                        r2 = [float(extent.strip('%')) for extent in extents_2] 
                        # Checking for overlapping rectangles
                        if l1[0] < r2[0] and r1[0] > l2[0] and l1[1] > r2[1] and r1[1] < l2[1]:
                            raise OverlappingActiveElementsError(self)
    
 
    def is_in_segment(self, begin=None, end=None):
        if begin is not None:
            if self.computed_end_time is not None and self.computed_end_time <= begin:
                return False
        if end is not None:
            if self.computed_begin_time >= end:
                return False
        return True

    def _assert_in_segment(self, dataset, element_content=None):
        if not self.is_in_segment(
            begin=dataset['segment_begin'],
            end=dataset['segment_end']
        ):
            raise OutsideSegmentError()

    def is_timed_leaf(self):
        return False

    def _semantic_copy_apply_leaf_timing(self, copied_instance, dataset ,element_content=None):
        if not copied_instance.is_timed_leaf():
            copied_instance.begin = None
            copied_instance.end = None
            if hasattr(copied_instance, 'dur'):
                copied_instance.dur = None
        else:
            tt_elem = dataset['tt_element']
            trimmed_begin = self.computed_begin_time
            trimmed_end = self.computed_end_time
            segment_begin = dataset['segment_begin']
            segment_end = dataset['segment_end']
            if segment_begin is not None:
                if segment_begin > trimmed_begin:
                    trimmed_begin = segment_begin
            if segment_end is not None:
                if trimmed_end is None or trimmed_end > segment_end:
                    trimmed_end = segment_end

            # Create compatible timing types
            copied_instance.begin = tt_elem.get_timing_type(trimmed_begin)
            copied_instance.end = tt_elem.get_timing_type(trimmed_end)


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
