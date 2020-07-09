@styles @document @simple
Feature: Compute style attribute on a single EBU-TT Live element

  Examples:
  | xml_file                      | cell_resolution | extent      |
  | style_attribute_inherited.xml | 32 15           | 320px 150px |


  # Inheritance: region (S1) > div (S2) > p (S3) > span (S4)
  Scenario: Simple (non-inheritable) style attributes
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And R1 contains <style_attribute> value <R1_value>
    And it contains style S1 with <style_attribute> value <S1_value>
    And it contains style S2 with <style_attribute> value <S2_value>
    And it contains style S3 with <style_attribute> value <S3_value>
    And it contains style S4 with <style_attribute> value <S4_value>
    And the document is generated
    Then the computed <style_attribute> in <elem_id> is <computed_value>

    Examples:
    | R1_value | S1_value  | S2_value | S3_value       | S4_value | style_attribute     | elem_id | computed_value |
    # default value:
    |          |           |          |                |          | tts:backgroundColor | span1   | transparent    |
    # does not inherit from region:
    |          | blue      |          |                |          | tts:backgroundColor | span1   | transparent    |
    # does not inherit from parent:
    |          |           |          | blue           |          | tts:backgroundColor | span1   | transparent    |
    # does compute if specified directly:
    |          |           |          |                | blue     | tts:backgroundColor | span1   | blue           |
    |          |           |          |                |          | tts:padding         | span1   | 0px            |
    |          |           |          |                | 10px     | tts:padding         | span1   | 10px           |
    |          | 10px      |          |                |          | tts:padding         | span1   | 0px            |
    |          | 10px      |          |                |          | tts:padding         | R1      | 10px           |
    # padding defined directly on region overrides S1:
    | 10px     | 20px      |          |                |          | tts:padding         | R1      | 10px           |
    |          |           |          |                |          | tts:unicodeBidi     | span1   | normal         |
    |          |           |          | embed          |          | tts:unicodeBidi     | span1   | normal         |
    |          |           |          |                | embed    | tts:unicodeBidi     | span1   | embed          |
