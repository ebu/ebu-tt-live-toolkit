Timing resolution and consumer logic
====================================

EBU-TT part 3 deals with sequences of documents and uses those combined to create a single timeline/sequence where
document contents(ISD) begin and end events are kept. Resolving this takes resolving the document timings first.
After each document's internal timing relationships have been worked out the document is getting inserted into the
timeline where possible collisions are detected and resolved with the possible discarding of documents in the process.

Document Timings
----------------

The document timing resolution logic is built using the validation framework and mostly is in
:py:class:`ebu_tt_live.bindings.validation.TimingValidationMixin`

The approach is that the element timing semantics require parent and children derived information to calculate
begin and end events on an absolute timeline. For this we hook into the Depth First Search the validation framework
uses to process element validation. It is very important to notice that the begin and end times are possible to be
calculated either as the algorithm cascades down or on its way up in case information derived from children is required.

.. graphviz:: dfs.dot

Sequence Timings
----------------

The sequence timings are handled by the :py:class:`ebu_tt_live.documents.ebutt3.EBUTT3DocumentSequence` class.
The document is insterted after having been validated into the sequence. The sequence looks at the computed begin and
end times and detects collisions. If there are any the collisions are resolved by the logic starting in
:py:function:`ebu_tt_live.documents.ebutt3.EBUTT3DocumentSequence._insert_or_discard`