@styles @document
Feature: Compute padding on a single EBU-TT Live element
 
  # tts:padding may appear both in the tt:style and tt:region element.
  # The padding property shall not be inherited. To apply padding to tt:p and tt:span elements, a tt:style element shall be referenced by tt:p or tt:span.
  # Percentage relative to width and height of region.

  Examples:
  | xml_file    | cell_resolution | style_attribute | elem_id |  
  | padding.xml | 10 10           | tts:padding     | region1 |  


  # Inheritence: region (S1) > div (S2) > p (S3) > span (S4)
  # tts:extent="100% 100%"
  Scenario: padding
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it contains style S1 with <style_attribute> value <S1_value>
    And it contains <style_attribute> value <S2_value> applied to region
    And the document is generated
    Then the computed <style_attribute> in <elem_id> is <computed_value>

    Examples:
    | S1_value | S2_value       | computed_value  |  
    | 1%       | 5%             | 5%              |  
    | 1c 1c    |                | 10% 10% 10% 10% |  
    |          | 1c .5c 1c 0.5c | 10% 5% 10% 5%   |  
    
    


