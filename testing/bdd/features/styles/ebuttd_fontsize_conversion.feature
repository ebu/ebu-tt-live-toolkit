@styles @document @ebuttd_conversion @fontSize
Feature: Compute fontSize on a single EBU-TT Live element

  Examples:
  | style_attribute | local_time_mapping |
  | tts:fontSize    | 00:00:00           |

  # Elements referencing styles with different fontSize attribute values
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
    | xml_file                      | extent | cell_resolution | S1_value | S2_value | S3_value | S4_value  | S5_value | S6_value |
    | ebuttd_fontsize_convert.xml   |        | 32 15           | 100%     | 100%     | 100%     | 100%      | 100%     | 100%     |
    | ebuttd_fontsize_convert.xml   |        | 32 15           | 50%      | 100%     | 100%     | 100%      | 1c       | 1c       |



  # If specified in cell units, the computation must take into account cellResolution.
  # If not region element, calculation is relative to parent element's font size; otherwise, relative to the Computed Cell Size.
  # The second value for font size is ignored in the conversion.

  # TODO: Fix this test
#  @skip
#  Scenario: Inherited font size calculation
#    Given an xml file <xml_file>
#    When it has a cell resolution of <cell_resolution>
#    And it has extent of <extent>
#    And element <live_parent> with <style_attribute> value of <live_parent_fontSize>
#    And child element with tts:fontSize <live_child_fontSize>
#    And we convert to an EBU-TT-D document with cell resolution <ttd_cell_resolution> and <local_time_mapping>
#    Then the EBU-TT-D has parent element <ttd_parent> with applied font size <ttd_parent_fontSize>
#    And a child element with applied font size <ttd_child_fontSize>
#
#  Examples:
#  | cell_resolution | extent  | live_parent | live_parent_fontSize | live_child_fontSize | ttd_cell_resolution | ttd_parent | ttd_parent_fontSize | ttd_child_fontSize |
#  | 32 15                |              | tt:p        | 1c                   | 100%                | 32 15               | tt:p       | 100%                | 100%               |
#  | 32 15                |              | tt:region   | 100%                 | 200%                | 32 15               | tt:region  | 100%                | 200%               |
#  | 64 30                |              | tt:region   | 200%                 | 50%                 | 32 15               | tt:region  | 100%                | 50%                |
#  | 32 15                |              | tt:p        | 1c 1c                | 2c                  | 32 15               | tt:p       | 100%                | 200%               |
#  | 32 15                |              | tt:region   | 1c 2c                | 50%                 | 32 15               | tt:region  | 100%                | 50%                |
#  | 64 30                |              | tt:p        | 200%                 | 1c                  | 32 15               | tt:p       | 100%                | 50%                |
#  | 32 15                | 1280px 720px | tt:p        | 48px                 | 24px                | 32 15               | tt:p       | 100%                | 50%                |
#  | 32 15                | 1280px 720px | tt:region   | 1c 2c                | 48px                | 32 15               | tt:region  | 100%                | 100%               |
#  | 20 10                | 1280px 720px | tt:p        | 72px 100px           | 50%                 | 40 20               | tt:p       | 200%                | 50%                |
