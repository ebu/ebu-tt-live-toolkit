@styles @document @fontSize
Feature: Compute fontSize on a single EBU-TT Live element

  # fontSize behaves in a special way compared to the other style attributes as it
  # not only inherits, in the case of percentage values it also cascades on computed fontSize
  # values defined in the parent elements of the element in question.

  Examples:
  | xml_file                      | elem_id | style_attribute |  
  | style_attribute_inherited.xml | span1   | tts:fontSize    |  

  # Elements referencing styles with different fontSize attribute values
  # Inheritence: region (S1) > div (S2) > p (S3) > span (S4)
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
    | extent      | cell_resolution | S1_value | S2_value | S3_value | S4_value  | computed_value |
    |             | 32 15           | 50%      | 200%     | 50%      | 200%      | 1c             |
    |             | 32 15           | 100%     | 100%     | 100%     | 100%      | 1c             |
    |             | 32 15           | 1c       | 200%     | 100%     | 50%       | 1c             |
    |             | 32 15           | 100%     | 2c       | 100%     | 50%       | 1c             |
    |             | 10 10           | 100%     |          |          | 50%       | .5c            |
    | 100px 100px | 10 10           | 1c 2c    | 100% 50% | 5px 20px | 200% 50%  | 1c 1c          |
    |             | 10 10           |          | 50%      |          | 400%      | 2c             |
    |             | 10 10           | 1c 2c    | 100% 50% | 50% 100% | 200% 100% | 1c 1c          |
    # implicit cell resolution of 32 15:
    | 100px 100px |                 |          | 10px     | 200%     | 50%       | 1.5c           |


