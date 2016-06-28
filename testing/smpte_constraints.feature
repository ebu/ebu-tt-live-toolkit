Feature: SMPTE-related attribute constraints
  Scenario: Valid SMPTE head attributes
    Given an xml file <xml_file>
    And it has frameRate <frame_rate>
    And it has timeBase <time_base>
    Then document is valid

    Examples:
    | xml_file   | frame_rate | time_base |
    | smpte.xml  | 25         | smpte     |
    | smpte.xml  | 20         | smpte     |

  # These tests are not all passing because the missing semantic validation piece
  Scenario: Invalid SMPTE head attributes
    Given an xml file <xml_file>
    And it has frameRate <frame_rate>
    And it has timeBase <time_base>
    Then document is invalid

    Examples:
    | xml_file   | frame_rate | time_base |
    | smpte.xml  |            | smpte     |
    | smpte.xml  | 25         | clock     |