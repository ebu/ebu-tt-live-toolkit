@styles @document @lineHeight
Feature: lineHeight relative to fontSize

  # The lineHeight attribute is a special case because of its relative semantics to fontSize.
  # In the simplest cases it is some pixel or cell value which is explicit. In the percentage case
  # it relates to the computed fontSize of the element in question.
  # If the value is specified as normal, which also happens to be the default according to 3350 it should be
  # as big as the biggest fontSize used in child elements.

  # NOTE: computing 'normal' explicitly is currently beyond the scope of this project. The computed value shall
  # remain 'normal' in that case. In all the rest of the cases the computed value is based on cell units.

  Examples:
  | xml_file                  | style_attribute | style_attribute2 | cell_resolution | extent      |
  | style_attribute_pairs.xml | tts:lineHeight  | tts:fontSize     | 32 15           | 320px 150px |

  # Inheritance: region (S1) > div (S2) > p (S3) > span (S4)
  Scenario: lineHeight computed values
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it contains style S1 with <style_attribute> value <S1_value>
    And S1 contains <style_attribute2> value <S1_value2>
    And it contains style S2 with <style_attribute> value <S2_value>
    And S2 contains <style_attribute2> value <S2_value2>
    And it contains style S3 with <style_attribute> value <S3_value>
    And S3 contains <style_attribute2> value <S3_value2>
    And it contains style S4 with <style_attribute> value <S4_value>
    And S4 contains <style_attribute2> value <S4_value2>
    And the document is generated
    Then the computed <style_attribute> in <elem_id> is <computed_value>

    Examples:

    | S1_value | S1_value2 | S2_value | S2_value2 | S3_value | S3_value2 | S4_value | S4_value2 | elem_id | computed_value |
    |          |           |          |           |          |           |          |           | p1      | normal         |
    | 1c       |           |          |           |          |           |          |           | p1      | 1c             |
    | 1c       |           | 2c       |           |          |           |          |           | p1      | 2c             |
    # Independence of fontSize:
    | 1c       | 3c        | 2c       | 3c        |          |           |          |           | p1      | 2c             |
    # Independence of fontSize:
    | 1c       | 3c        | 20px     | 3c        |          |           |          |           | p1      | 2c             |
    # Dependence of fontSize:
    | 1c       | 2c        | 100%     | 3c        |          |           |          |           | p1      | 3c             |
    # Dependence of fontSize:
    | 1c       | 2c        | 100%     | 30px      |          |           |          |           | p1      | 3c             |
    # Dependence of fontSize in the same context:
    | 100%     | 2c        |          | 3c        |          |           |          |           | p1      | 2c             |
    # lineHeight and fontSize on span are ignored, p fontSize inherited:
    | normal   | 1c        | 100%     | 2c        | 150%     |           | 50%      | 4c        | p1      | 3c             |
