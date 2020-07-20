@styles @document @ebuttd_conversion @fontSize
Feature: Convert fontSize from EBU-TT Live to EBU-TT-D where inherited font sizes are present.

  Examples:
  | local_time_mapping | xml_file                      |
  | 00:00:00           | ebuttd_fontsize_inherited.xml |

  # Each of region, div, and p can have different font sizes specified in different units.
  # These are specified by referencing different style elements, unlike the same style ref feature.
  # The converted output sets percentage unit single value font sizes only.
  # Output font sizes of 100% are removed.
  # If specified in cell units, the computation must take into account cellResolution.
  # If not region element, calculation is relative to parent element's font size; otherwise, relative to the Computed Cell Size.
  # The (first) horizontal component of two component font sizes is ignored in the conversion.

  Scenario: Inherited font size calculation
    Given an xml file <xml_file>
    When it has a cell resolution of <cell_resolution>
    And it has extent of <extent>
    And it has region fontSize of <region_fontSize>
    And it has div fontSize of <div_fontSize>
    And it has p fontSize of <p_fontSize>
    And the document is generated
    And the document is converted to EBUTTD with <local_time_mapping>
    Then EBUTTD document is valid
    And the EBUTTD has region fontSize <ttd_region_fontSize>
    And the EBUTTD has div fontSize <ttd_div_fontSize>
    And the EBUTTD has p fontSize of <ttd_p_fontSize>

  Examples:
  | cell_resolution | extent       | region_fontSize | div_fontSize | p_fontSize | ttd_region_fontSize | ttd_div_fontSize | ttd_p_fontSize |
  | 40 24           |              |                 | 1c 2c        | 1c 2c      |                     | 200%             |                |
  | 32 15           |              |                 | 1c           | 100%       |                     |                  |                |
  | 32 15           |              | 100%            |              | 200%       |                     |                  | 200%           |
  | 32 15           |              |                 | 1c 1c        | 2c         |                     |                  | 200%           |
  | 32 15           |              | 1c 2c           |              | 50%        | 200%                |                  | 50%            |
  | 32 15           | 1280px 720px |                 | 48px         | 24px       |                     |                  | 50%            |
  | 32 15           | 1280px 720px | 1c 2c           |              | 48px       | 200%                |                  | 50%            |

# TODO: if we implement different output EBU-TT-D cell resolution compared to input, these tests are relevant (but need to be checked).
#  | cell_resolution | extent       | region_fontSize | div_fontSize | p_fontSize | ttd_cell_resolution | ttd_region_fontSize | ttd_div_fontSize | ttd_p_fontSize |
#  | 64 30           |              | 200%            |              | 50%        | 32 15               | 100%                | 50%              |                |
#  | 64 30           |              |                 | 200%         | 1c         | 32 15               |                     | 100%             | 50%            |
#  | 20 10           | 1280px 720px |                 | 72px 100px   | 50%        | 40 20               |                     | 200%             | 50%            |
