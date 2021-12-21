Denesting of EBU-TT-Live documents
======================================

DenesterNode should be used when a EBU-TT-3 document has a div that contains
other divs, or a span contains another span, and those nested elements need
to be flattened, for example before conversion to EBU-TT-D. These elements
are not able to be nested inside each other in EBU-TT-D documents.

When documents are Denested, any nested elements must be removed from
their parent elements, while retaining attributes they would have inherited.
To address this, the DenesterNode node processes the
document(s) with the
:py:func:`ebu_tt_live.node.denester.DenesterNode.recurse` and
:py:func:`ebu_tt_live.node.denester.DenesterNode.recurse_span`
functions. These will iterate through the file to locate the deepest
nested element, and create a new copy of it with its content and
expected inherited attributes. The end result is a file containing
these newly created divs/spans in place of the nested ones.

Once the new divs and spans are created, divs that are sequential in
the list of divs and have the same attributes are combined into a single
div. This is done by the
:py:func:`ebu_tt_live.node.denester.DenesterNode.combine_divs`
function to reduce the number of divs in the resulting file.

In the combined divs, every p element should have the same region
as its parent div. Any p elements that specify a different region
to their inherited region are removed here: as per TTML semantics,
such p elements are never presented.
The
:py:func:`ebu_tt_live.node.denester.DenesterNode.check_p_regions`
function iterates through the divs that have an assigned region and
removes any p where its region does not match.
It then removes the region attribute from any remaining p, as it will
inhert the region of its parent div and the attribute is unnecessary.
It will also remove any now-empty divs that exist as a result of having
their p elements removed.
