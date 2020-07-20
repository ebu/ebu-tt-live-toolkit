@styles @document @ebuttd_conversion @fontSize
Feature: Convert fontSize from EBU-TT Live to EBU-TT-D when two elements reference the same style

  Examples:
  | local_time_mapping | xml_file                           | style_attribute | style_attribute2 |
  | 00:00:00           | ebuttd_fontsize_same_style_ref.xml | tts:fontSize    | tts:lineHeight   |

  # Both the div and the p in the XML file reference style S1, unlike the fontsize inheritance test.
  # The fontSize can be set on the input in different units.
  # The converted output sets percentage unit single value font sizes only.
  # Output font sizes of 100% are removed.
  # If not region element, calculation is relative to parent element's font size; otherwise, relative to the Computed Cell Size.
  # The (first) horizontal component of two component font sizes is ignored in the conversion.

  Scenario: Inherited font size calculation
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it contains style S1 with <style_attribute> value <S1_value>
    And S1 contains <style_attribute2> value <S1_value2>
    And the document is generated
    And the document is converted to EBUTTD with <local_time_mapping>
    Then EBUTTD document is valid
    And the EBUTTD has div fontSize <ttd_div_fontSize>
    And the EBUTTD has div lineHeight of <ttd_div_lineHeight>
    And the EBUTTD has p fontSize of <ttd_p_fontSize>
    And the EBUTTD has p lineHeight of <ttd_p_lineHeight>

  Examples:
  | cell_resolution | extent       | S1_value | S1_value2 | ttd_div_fontSize | ttd_div_lineHeight | ttd_p_fontSize | ttd_p_lineHeight |
  | 40 24           |              | 1c 2c    |           | 200%             |                    |                |                  |
  | 32 15           |              | 1c       |           |                  |                    |                |                  |
  | 32 15           |              | 2c       |           | 200%             |                    |                |                  |
  | 32 15           |              | 100%     |           |                  |                    |                |                  |
  | 32 15           |              | 200%     |           | 200%             |                    | 200%           |                  |
  | 32 15           |              |          |           |                  |                    |                |                  |
  | 32 15           | 1280px 720px | 24px     |           | 50%              |                    |                |                  |
  | 32 15           | 1280px 720px | 48px     |           |                  |                    |                |                  |
  | 40 24           |              | 1c 2c    | normal    | 200%             |                    |                |                  |
  | 32 15           |              | 1c       | normal    |                  |                    |                |                  |
  | 32 15           |              | 2c       | normal    | 200%             |                    |                |                  |
  | 32 15           |              | 100%     | normal    |                  |                    |                |                  |
  | 32 15           |              | 200%     | normal    | 200%             |                    | 200%           |                  |
  | 32 15           |              |          | normal    |                  |                    |                |                  |
  | 32 15           | 1280px 720px | 24px     | normal    | 50%              |                    |                |                  |
  | 32 15           | 1280px 720px | 48px     | normal    |                  |                    |                |                  |
  | 40 24           |              | 1c 2c    | 120%      | 200%             | 120%               |                |                  |
  | 32 15           |              | 1c       | 120%      |                  | 120%               |                |                  |
  | 32 15           |              | 2c       | 150%      | 200%             | 150%               |                |                  |
  | 32 15           |              | 100%     | 120%      |                  | 120%               |                |                  |
  | 32 15           |              | 200%     | 120%      | 200%             | 120%               | 200%           | 120%             |
  | 32 15           |              |          | 120%      |                  | 120%               |                |                  |
  | 32 15           | 1280px 720px | 24px     | 120%      | 50%              | 120%               |                |                  |
  | 32 15           | 1280px 720px | 48px     | 120%      |                  | 120%               |                |                  |
  | 40 24           |              | 1c 2c    | 2.4c      | 200%             | 120%               |                |                  |
  | 32 15           |              | 1c       | 1.2c      |                  | 120%               |                |                  |
  | 32 15           |              | 2c       | 3c        | 200%             | 150%               |                |                  |
  | 32 15           |              |          | 150%      |                  | 150%               |                |                  |
  | 32 15           | 1280px 720px | 24px     | 28.8px    | 50%              | 120%               |                |                  |
  | 32 15           | 1280px 720px | 48px     | 57.6px    |                  | 120%               |                |                  |
