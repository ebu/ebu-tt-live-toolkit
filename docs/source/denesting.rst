Denesting of EBU-TT-Live documents
======================================

DenesterNode should be used when a EBU-TT-3 document has a div that contains
other divs, or a span contains another span, and those nested elements need
to be flattened, for example before conversion to EBU-TT-D. These elements
are not permitted to be nested inside each other in EBU-TT-D documents.

When documents are Denested, any nested elements must be removed from
their parent elements, while retaining attributes they would have inherited.
To address this, the DenesterNode node processes the
document(s) with the
:py:func:`ebu_tt_live.node.denester.DenesterNode.recurse` and
:py:func:`ebu_tt_live.node.denester.DenesterNode.recurse_span`
functions. These iterate through the file to locate the deepest
nested ``div`` and ``span`` elements,
and create a new copy of it with its content and
expected inherited attributes.
Where necessary new ``div`` or ``span`` elements are synthesised to wrap
content that is `not` wrapped as deeply as its adjacent content. The end result is a file containing
these newly created ``div`` s and ``span`` s in place of the nested ones,
ensuring all content is in the correct order.

Any content elements whose region differs from its inherited region are pruned
by the Denester.

Merging metadata
----------------

If a ``div`` element *d1* contains a ``metadata`` child with some metadata in it,
*and* a ``div`` *d1_1* element which *also* contains a ``metadata`` child with
some different metadata in it, how shall we merge them together?

Unlike time, lang, style or region attributes where the computed effect is
specified by the TTML specification, there is no such defined semantic for
computing metadata; there are no inheritance rules for example, in general.
Our choices were to discard some metadata or try to keep it all at the risk of
it not making sense.

The denester code currently merges metadata by concatenating the lists of
child elements of the metadata elements in order of least nested to most nested
parent element. In other words an input with::

 <div>
   <metadata>
     <foo:bar>First</foo:bar>
   </metadata>
   <div>
     <metadata>
       <foo:bar>Second</foo:bar>
     </metadata>
     <p xml:id="p0">Some content</p>
   </div>
 </div>

will generate an output like::

 <div>
   <metadata>
     <foo:bar>First</foo:bar>
     <foo:bar>Second</foo:bar>
   </metadata>
   <p xml:id="p0">Some content</p>
 </div>


Implementation details
----------------------

:py:func:`ebu_tt_live.node.denester.DenesterNode.recurse` generates a complete
ordered list of ``div`` elements, but it does so in a brutish sort of way:
*every* descendant ``p`` element gets a single parent ``div`` element.

It is important that the computed values of time, lang, style and region are
the same in the unnested divs as they would be in the input document, in other
words, that the attributes that the ``p`` children inherit are identical.
:py:func:`ebu_tt_live.node.denester.DenesterNode.merge_attr` takes care of
this processing.

Having one ``div`` element per ``p`` child is not desirable in the output,
so after doing this any adjacent ``div`` s
that have the same set of "attributes" are combined. The test for whether
two adjacent ``div`` s are combinable checks attributes for
style, region, begin and end times and xml:lang and also the contents of the
``metadata`` element).
:py:func:`ebu_tt_live.node.denester.DenesterNode.combine_divs` takes care of
this combination of ``div`` elements.

The code for processing nested ``span`` s is a little
different. This is handled in 
:py:func:`ebu_tt_live.node.denester.DenesterNode.recurse_span`.
Again, we could create a new ``span`` for every piece of character content
and ``br`` element (and foreign namespace elements), and then combine
adjacent ones, however instead we merge as we go along, appending new
content to a "working" copy of a span as we iterate through, and then
closing this off if we encounter a new child ``span``.

Sometimes new styles are needed to represent the computed value of the
styles of a nested element. The Denester remembers any styles it needs to
make and tries to reuse them.

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

Removing elements from their parent in pyxb
-------------------------------------------

During implementation and testing we noticed that validating documents
generated by the Denester sometimes generated a lot of info-level log
messages similar to::

 orphan <pyxb.binding.basis.ElementContent object at 0x7f7fdc77ea90> in content

The cause of this was that when the Denester code removed a ``span``
element from its parent ``p`` or ``span`` some memory of the removed
element remained.

pyxb maintains both an ordered list of all child elements, which can
be obtained by calling ``.orderedContent()`` on the element, *and* a
list of each type of child element where there can be more than one.

We learned that calling ``[span or p object].span.clear()`` clears all
the ``span`` children associated with the span binding location,
but leaves them in the list of ordered content. The ``validate()``
function then discovers the discrepancy and tries to tidy up, giving
these strange log messages.

We resolved this by creating a complete new list of the elements that
we want to be the children of the parent element, and then clearing
*both* the binding points for plural elements *and* the existing
ordered content list, and then appending all the desired child elements
by calling ``[object].extend(new_ordered_content)``.

Removing elements from pyxb binding objects can be done, but it's more
complex than adding or changing them, and somewhat less intuitive!