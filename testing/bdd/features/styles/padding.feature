@styles @document
Feature: Compute padding on a single EBU-TT Live element
 
  # tts:padding may appear both in the tt:style and tt:region element.
  # The padding property shall not be inherited. To apply padding to tt:p and tt:span elements, a tt:style element shall be referenced by tt:p or tt:span.
  # Percentage relative to width and height of region.# Elements referencing styles with different padding attribute values

  Examples:
  | elem_id | attribute   | xml_file    |  
  | region1 | tts:padding | padding.xml |  
  
  Scenario: Font size inheritance 
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it contains a region with applied <attribute> set to <value_1>
    And the region contains inline <attribute> value <value_2>
    And the document is generated
    Then the computed <attribute> for <elem_id> is <computed_value>

    # In the template the region is defined with: tts:origin="0 0" tts:extent="100% 100%" 
    Examples:
    | cell_resolution | extent      | value_1 | value_2        | computed_value      |  
    | 10 10           | 100px 100px | 1%      | 5%             | 5px                 |  
    | 10 10           | 100px 100px | 1c 1c   |                | 10px 10px 10px 10px |  
    | 10 10           | 100px 100px |         | 1c .5c 1c 0.5c | 10px 5px 10px 5px   |  
    
    


