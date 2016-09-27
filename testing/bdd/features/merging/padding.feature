@styles @document
Feature: Compute padding on a single EBU-TT Live element

  # tts:padding may appear both in the tt:style and tt:region element.
  # The padding property shall not be inherited. To apply padding to tt:p and tt:span elements, a tt:style element shall be referenced by tt:p or tt:span.
  # Percentage relative to width and height of region.
  Scenario: Padding on region and descendents
    Given an EBU-TT Live document <xml_file>
    And the document has a cell resolution of <cell_resolution>
    And the document contains a region sized <region_extent> 
    And the region has applied padding <region_padding>
    And the document contains a div that refereces the region
    And the div references a style with padding <div_padding>
    And the div has a child p that references a style with padding <p_padding>
    And the p has a child span that references a style with padding <span_padding>
    When the span contains text
    Then the computed padding for the text is <computed_padding>

    Examples:
    | xml_file    | cell_resolution | region_extent | region_padding | div_padding | p_padding | span_padding | computed_padding |  
    | padding.xml |                 | 100% 100%     | 1%             |             |           |              | 1%               |  

