@styles @document @ebuttd_conversion @fontSize
Feature: Compute fontSize on a single EBU-TT Live element

  Examples:
  | xml_file                      | extent | cell_resolution | style_attribute | local_time_mapping |
  | ebuttd_fontsize_convert.xml   |        | 40 22           | tts:fontSize    | 00:00:00           |

  # Elements referencing styles with different fontSize attribute values
  # This feature tests that valid output is generated, but does not check
  # that the output is correct. The fontsize inheritance and fontsize same style ref
  # features check for correct output too.
  Scenario: Font size inheritance
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it contains style S1 with <style_attribute> value <S1_value>
    And it contains style S2 with <style_attribute> value <S2_value>
    And it contains style S3 with <style_attribute> value <S3_value>
    And it contains style S4 with <style_attribute> value <S4_value>
    And it contains style S5 with <style_attribute> value <S5_value>
    And it contains style S6 with <style_attribute> value <S6_value>
    And the document is generated
    And the document is converted to EBUTTD with <local_time_mapping>
    Then EBUTTD document is valid

    # TODO: implement the rest of the assertions once EBUTTD has some semantic validation of sorts...

    Examples:
    | S1_value | S2_value | S3_value | S4_value  | S5_value | S6_value |
    | 100%     | 100%     | 100%     | 100%      | 100%     | 100%     |
    | 50%      | 100%     | 100%     | 100%      | 1c       | 1c       |
