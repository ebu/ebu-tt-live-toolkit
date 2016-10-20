

The problem
-----------

Convert an EBU-TT part 3 document to EBU-TT-D

EBU-TT part 3 uses fonSize in 3 datatypes: cells, pixels and percentage.
EBU-TT-D uses percentage fontSize only and prohibits pixels.

In order to be converted the sizes need to be translated from pixels/cells to percentages.

### Percentages vs. pixels/cells
  The relationship between parent and child element is important when percentages are used as the child modulates the computed fontSize of the parent container, however it is an override when it comes to the other 2 types.
  In order to be converted an absolute size needs to be calculated. According to TTML the [computed fontSize](http://w3c.github.io/ttml2/spec/ttml2.html#semantics-style-resolved-value-category-computed) value is an absolute value such as pixel. This poses a problem of tt@extent not always being available to us. cellResolution is available, as it has a default value and pixelAspectRatio is available as it has a default value.
  
### Percentages and the EM square
  When the top level fontSize attribute is evaluated (say on the region) If it is a percentage value of 100% 100% the default fontsize EM square is scaled by maintaining its aspect ratio producing a square. ?? Is this true http://w3c.github.io/ttml2/spec/ttml2.html#style-attribute-fontSize seems to be contradictory on this matter ??
  Then only one value of 100% is provided according to TTML I am supposed to assume 100% 100% that gives the same square result.
  
  Let's look at 1c 1c. Since we have a cellResolution of 32:15 this should mean that the EM square is anamorphically scaled to 1c 1c assuming that the pixelAspectRatio is 1:1 and extent width:extent height != 32:15 (The root container region is not a square)
  If we see 1c and take TTML's suggestion of that being 1c 1c, then the same anamorphic scaling is applied as above.
  
  At this point there is a big difference of the default value assumption. Depending on what unit I assume the default value in
  the results are different. 
  
#### More complications around children wth percentages
  
  Let's assume we have the following styles at hand:
      
      <style id="S1c" fontSize="1c"/>
      <style id="S100p" fontSize="100%"/>
      <style id="S1c1c" fontSize="1c 1c"/>
      <style id="S50p" fontSize="50%"/>
      <style id="S20p50p" fontSize="20% 50%"/>

##### Example 1:
    
    <div style="S50p">
      <p style="S20p50p">Test text</p>
    </div>
    
  This is a clear case of the default EM Square going to half of its height and half its width and then anamorphically scaled to 20%:50%
  
##### Example 2:

    <div style="S1c1c">
      <p style="S20p50p">Test text</p>
    </div>
    
  This is 2 anamorphic scaling steps quite clear.
  
##### Example 3:

    <div style="S1c">
      <p style="S20p50p">Test text</p>
    </div>
    
  The intuitive assumption would be here that we have a default EM square of a 1c tall glyph that is going to be scaled to 20:50. 
  But according to TTML's definition this case is the same as the case above because we are to assume 1c 1c.
   
#### What if we could figure out width from height

  This seems to be an obvious wish by now if we could work out a way to normalize our sizing to be always 2 dimensional and have simple algorithms deal with them without having to cater for edge cases of S100p being completely different from S1c.
  In order for us to do that the following values are all required:
  
    extent(in pixels), cellResolution, pixelAspectRatio
    
  In a processing pipeline where we would like to convert subtitle formats from one format to another having to know about the presentation context of a rendering engine is not quite ideal. I am unsure what the solution here is but this clearly creates a problem.
  
  
