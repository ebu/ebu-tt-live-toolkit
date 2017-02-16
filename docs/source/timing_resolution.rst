Timing resolution and consumer logic
====================================

EBU-TT part 3 deals with sequences of documents and creates a single timeline/sequence where
document begin and end events are kept. Resolving this takes resolving the document timings first.
After each document's internal timing relationships have been worked out the document is inserted into the
timeline where possible collisions are detected and resolved with the possible discarding of documents in the process.

Document Timings
----------------

The document timing resolution logic is built using the validation framework and mostly is in
:py:class:`ebu_tt_live.bindings.validation.TimingValidationMixin`

The approach is that the element timing semantics require parent and children derived information to calculate
begin and end events on an absolute timeline. For this we hook into the Depth First Search that the validation framework
uses to process element validation. It is very important to note that the begin and end times can be
calculated either as the algorithm cascades down or on its way up in case information derived from children is required.

.. graphviz:: dot/dfs.dot

The classes involved in the timing resolution are in the diagram below. For every type of element in the XSD there is
a python binding class defined. For the sake of simplicity the diagram only contains a fraction of them to provide
enough context but omits the parts that are irrelevant to the timing resolution logic.

.. uml:: timing_class_diagram.puml
   :caption: Classes involved in timing resolution (Simplified)

The functions :py:func:`ebu_tt_live.bindings.validation.base.SemanticDocumentMixin._semantic_before_validation` and
:py:func:`ebu_tt_live.bindings.validation.base.SemanticDocumentMixin._semantic_after_validation` are hooks that run
before and after the Depth First Search traversal of the content tree.
The :py:func:`ebu_tt_live.bindings.validation.base.SemanticValidationMixin._semantic_before_traversal` and
:py:func:`ebu_tt_live.bindings.validation.base.SemanticValidationMixin._semantic_after_traversal` are element hooks,
which are called before the traversal logic gets to the element and after the traversal logic has finished processing
the children of the element in question. Types that subclass these mixins should override these functions to provide
their own customized hook behaviour. In the case of timing resolution another mixin,
:py:class:`ebu_tt_live.bindings.validation.base.TimingValidationMixin` is involved, which encapsulates the functions
used to process `begin` and `end` attributes. In order for a particular element type to gain timing resolution
capability it needs to subclass `TimingValidationMixin` and `SemanticValidationMixin` and it must have `begin` and `end`
attributes capability. Then it should implement `_semantic_before_traversal` and `_semantic_after_traversal` functions
and call the :py:class:`ebu_tt_live.bindings.validation.timing.TimingValidationMixin._semantic_preprocess_timing`
in the before traversal and
:py:class:`ebu_tt_live.bindings.validation.timing.TimingValidationMixin._semantic_postprocess_timing` in the after
traversal hook. The following code sample is from the implementation of the div_type class.

.. code-block:: python

    def _semantic_before_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_register_id(dataset=dataset)
        self._semantic_timebase_validation(dataset=dataset, element_content=element_content)
        self._semantic_preprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_set_region(dataset=dataset, region_type=region_type)
        self._semantic_collect_applicable_styles(
            dataset=dataset, style_type=style_type, parent_binding=parent_binding, defer_font_size=True
        )
        self._semantic_push_styles(dataset=dataset)

    def _semantic_after_traversal(self, dataset, element_content=None, parent_binding=None):
        self._semantic_postprocess_timing(dataset=dataset, element_content=element_content)
        self._semantic_unset_region(dataset=dataset)

In the following sequence diagram we traverse the document structure depicted in the first figure of this page and
process the timings.

.. uml:: timing_sequence_diagram.puml
   :caption: Timing validation of document tree (head element omitted as it is irrelevant to timing)

Sequence Timings
----------------

The sequence timings are handled by the :py:class:`ebu_tt_live.documents.ebutt3.EBUTT3DocumentSequence` class.
The document is insterted into the sequence after it is validated. The sequence looks at the computed begin and
end times and detects collisions. If there are any, the collisions are resolved by the logic starting in
:py:func:`ebu_tt_live.documents.ebutt3.EBUTT3DocumentSequence._insert_or_discard`
