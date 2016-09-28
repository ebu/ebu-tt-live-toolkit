@styles @document
Feature: Compute fontSize on a single EBU-TT Live element
 

  Examples:
  | elem_id | style_attribute |  
  | span1   | tts:fontSize    |  
  
  # Elements referencing styles with different fontSize attribute values
  Scenario: Font size inheritance 
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it contains a region with applied style S1 with <style_attribute> value <S1_value>
    And it contains a div with applied style S1 with <style_attribute> value <S2_value> that references the region
    And the div has a child p with applied style S3 with <style_attribute> value <S3_value>
    And the p has a child span with applied style S4 with <style_attribute> value <S4_value>
    And the document is generated
    Then the computed <style_attribute> in <elem_id> is <computed_value>

    Examples:
    | xml_file                      | extent      | cell_resolution | region_value | div_value | p_value  | span_value | computed_value |  
    | style_attribute_inherited.xml |             | 32 15           | 100%         | 100%      | 100%     | 100%       | 1c             |  
    | style_attribute_inherited.xml |             | 32 15           | 50%          | 200%      | 50%      | 200%       | 1c             |  
    | style_attribute_inherited.xml |             | 32 15           | 1c           | 200%      | 100%     | 50%        | 1c             |  
    | style_attribute_inherited.xml |             | 32 15           | 100%         | 2c        | 100%     | 50%        | 1c             |  
    | style_attribute_inherited.xml |             | 10 10           | 100%         |           |          | 50%        | .5c            |  
    | style_attribute_inherited.xml |             | 10 10           |              | 50%       |          | 400%       | 20%            |  
    | style_attribute_inherited.xml |             | 10 10           | 1c 2c        | 100% 50%  | 50% 100% | 200% 100%  | 10% 10%        |  
    | style_attribute_inherited.xml | 100px 100px |                 |              | 10px      | 200%     | 50%        | 10px           |  
    | style_attribute_inherited.xml | 100px 100px | 10 10           | 1c 2c        | 100% 50%  | 5px 20px | 200% 50%   | 1c             |  


  # One style references another style. Note that the ordering matters.
  # E.g:
  # <style xml:id="S1" tts:fontSize="100%" />             
  # <style xml:id="S2" style="S1" tts:fontSize="50%" />   // computed: 50%
  # <style xml:id="S3" tts:fontSize="50%" style="S1" />   // computed: 100%
  Scenario: Styles reference chain
    Given an xml file <xml_file>
    When the document has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And the document declares style S1 with font size <S1_value>
    And the document declares style S2 that references S1 then sets font size <S2_value> 
    And the document declares style S3 with font size <S3_value> then references S1
    And style <applied_style> is applied to text
    And the document is generated
    Then the computed <style_attribute> in <elem_id> is <computed_value>

    Examples:
    | xml_file     | cell_resolution | S1_value | S2_value  | S3_value | applied_style | computed_value |  
    | fontSize.xml | 32 15           | 100%     | 50%       | 100%     | S2            | 50%            |  
    | fontSize.xml | 32 15           | 100%     | 50%       | 100%     | S3            | 100%           |  
    | fontSize.xml | 10 10           | 100%     | 200%      | 50%      | S2            | 2c             |  
    | fontSize.xml | 10 10           | 100%     | 200%      | 50%      | S3            | 1c             |  
    | fontSize.xml | 10 10           | 100% 50% | 200% 100% | 50% 50%  | S2            | 2c 1c          |  
    | fontSize.xml | 10 10           | 100% 50% | 200%      | 50%      | S3            | 1c .5c         |  
