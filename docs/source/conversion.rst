Conversion of EBU-TT-Live documents to EBU-TT-D documents
=========================================================

The :py:func:`ebu_tt_live.documents.converters.ebutt3_to_ebuttd` function
creates an EBUTTDDocument from an EBUTT3Document using the helper class
:py:class:`ebu_tt_live.bindings.converters.ebutt3_ebuttd.EBUTT3EBUTTDConverter`.

This class manages various possible complications, including a significant set
of constraints about font size.

Here's some documentation from the coding process that captures some of our
internal conversation about how to map font sizes, to give an idea of the
complexity.

The problem
-----------

Convert an EBU-TT part 3 document to EBU-TT-D

EBU-TT part 3 uses fonSize in 3 datatypes: cells, pixels and percentage.
EBU-TT-D uses percentage fontSize only and prohibits pixels.

In order to be converted the sizes need to be translated from pixels/cells to
percentages. Percentages vs. pixels/cells

The relationship between parent and child element is important when percentages
are used as the child modulates the computed fontSize of the parent container,
however it is an override when it comes to the other 2 types. In order to be
converted an absolute size needs to be calculated. According to TTML the
computed fontSize value is an absolute value such as pixel. This poses a problem
of the ``tts:extent`` attribute of the ``tt:tt`` element not always being
available to us. ``ttp:cellResolution`` is available, because it has a default
value and ``ttp:pixelAspectRatio`` is available as it has a default value.

Percentages and the EM square
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider how the top level ``tts:fontSize`` attribute is evaluated (say on the
region). If it is a percentage value of ``"100%"`` then the EM square's
horizontal and vertical size are both the *height* of the cell whose size is
defined by the  ``ttp:cellResolution`` attribute of the ``tt:tt`` element.
However if it is a a percentage value of ``"100% 100%"`` then the EM square's
horizontal size is the *width* of a cell and its vertical size is the height of
a cell. Then any  derived size, say a ``tts:fontSize`` attribute specified on a
``style`` element  referenced by a ``tt:p`` element, is scaled in proportion to
its parent element's  font size (default is ``"100%"`` as defined above. See
http://w3c.github.io/ttml2/spec/ttml2.html#style-attribute-fontSize for the
definitive explanation in TTML2 (this is the same as TTML1 but with more recent
editorial additions).  

Let's look at ``"1c 1c"``. In general the cell is not square. In fact the only
case when it would be square would be if the ratio of the cell resolution's
horizontal and vertical components were the same as the ratio of the height and
the width of the rendering area. In pixels this would an equal height and width
if the pixels are square. If we see ``"1c"`` then the same anamorphic scaling is
applied as above. ``"1c 1c"`` is equivalent to ``"100% 100%"`` on the ``region``
element.

At this point there is a big difference of the default value assumption.
Depending on what unit I assume the default value in the results are different.

**More complications around children wth percentages**

Let's assume we have the following styles at hand: ::

  <style id="S1c" fontSize="1c"/>
  <style id="S100p" fontSize="100%"/>
  <style id="S1c1c" fontSize="1c 1c"/>
  <style id="S50p" fontSize="50%"/>
  <style id="S20p50p" fontSize="20% 50%"/>

Example 1: ::

  <div style="S50p">
    <p style="S20p50p">Test text</p>
  </div>

This is a clear case of the default EM Square going to half of its height and
half its width and then anamorphically scaled to 20%:50%

Example 2: ::

  <div style="S1c1c">
    <p style="S20p50p">Test text</p>
  </div>

This is 2 anamorphic scaling steps quite clear.

Example 3: ::

  <div style="S1c">
    <p style="S20p50p">Test text</p>
  </div>

Here we have a default EM square of a 1c
tall glyph that is going to be scaled in the ratio 20:50. 

**What if we could figure out width from height**

This seems to be an obvious wish by now if we could work out a way to normalize
our sizing to be always 2 dimensional and have simple algorithms deal with them
without having to cater for edge cases of S100p being completely different from
S1c. 

In order for us to do that the following values are all required: ::

  extent(in pixels), cellResolution, pixelAspectRatio

In a processing pipeline where we would like to convert subtitle formats from
one format to another having to know about the presentation context of a
rendering engine is not quite ideal. The solution here is not obvious but
this clearly creates a problem. 

The solution
------------

In the end we had to overload ``ebuttdt.PercentageFontSizeType`` to have either
one value or two value variants, and then deal with those cases in the
:py:func:`ebu_tt_live.bindings.converters.ebutt3_ebuttd.EBUTT3EBUTTDConverter._get_font_size_style`
function.
