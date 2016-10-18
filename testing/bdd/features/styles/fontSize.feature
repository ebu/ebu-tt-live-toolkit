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
    And it contains style S1 with <style_attribute> value <S1_value>
    And it contains style S2 with <style_attribute> value <S2_value>
    And it contains style S3 with <style_attribute> value <S3_value>
    And it contains style S4 with <style_attribute> value <S4_value>
    And the document is generated
    Then the computed <style_attribute> in <elem_id> is <computed_value>

    Examples:
    | xml_file                      | extent      | cell_resolution | S1_value | S2_value | S3_value | S4_value  | computed_value |  
    | style_attribute_inherited.xml |             | 32 15           | 100%     | 100%     | 100%     | 100%      | 1c             |
    | style_attribute_inherited.xml |             | 32 15           | 50%      | 200%     | 50%      | 200%      | 1c             |  
    | style_attribute_inherited.xml |             | 32 15           | 1c       | 200%     | 100%     | 50%       | 1c             |  
    | style_attribute_inherited.xml |             | 32 15           | 100%     | 2c       | 100%     | 50%       | 1c             |  
    | style_attribute_inherited.xml |             | 10 10           | 100%     |          |          | 50%       | .5c            |  
    | style_attribute_inherited.xml |             | 10 10           |          | 50%      |          | 400%      | 20%            |  
    | style_attribute_inherited.xml |             | 10 10           | 1c 2c    | 100% 50% | 50% 100% | 200% 100% | 10% 10%        |  
    | style_attribute_inherited.xml | 100px 100px |                 |          | 10px     | 200%     | 50%       | 10px           |  
    | style_attribute_inherited.xml | 100px 100px | 10 10           | 1c 2c    | 100% 50% | 5px 20px | 200% 50%  | 1c 1c          |


  # One style references another style. Note that the ordering matters.
  # E.g:
  # <style xml:id="S1" tts:fontSize="100%" />             
  # <style xml:id="S2" style="S1" tts:fontSize="50%" />   // computed: 50%
  # <style xml:id="S3" tts:fontSize="50%" style="S1" />   // computed: 100%
  @skip
  Scenario: Styles reference chain
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it has style S1 with <style_attribute> with value <S1_value> 
    And it has style S2 with <style_attribute> with value <S2_value> and <other_style_attribute> with value <other_style_value>
    And style S2 is applied to <elem_id>
    When the document is generated
    Then the computed value for <style_attribute> is <computed_value>

    Examples:
    | xml_file                | cell_resolution | extent      | S1_value  | S2_value  | other_style_attribute | other_style_value | computed_value |  
    | style_attribute_chained | 10 10           |             | 1c        | 2c        | style                 | S1                | 1c             |  
    | style_attribute_chained | 10 10           |             | 1c        | 2c        | tts:fontSize          | 3c                | 3c             |  
    | style_attribute_chained | 10 10           |             | 1c        |           | style                 | S1                | 1c             |  
    # Style 2 references itself:
    | style_attribute_chained | 10 10           | 100px 100px | 10px 20px | 20px 10px | style                 | S2                | 20px 10px      |  

