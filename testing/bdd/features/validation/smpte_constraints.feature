Feature: SMPTE-related attribute constraints
  Scenario: Valid SMPTE head attributes
    Given an xml file <xml_file>
    And it has frameRate <frame_rate>
    And it has timeBase <time_base>
    And it has frameRateMultiplier <frame_rate_multiplier>
    And it has dropMode <drop_mode>
    And it has markerMode <marker_mode>
    Then document is valid

    Examples:
    | xml_file   | frame_rate | time_base | frame_rate_multiplier | drop_mode | marker_mode   |
    | smpte.xml  | 25         | smpte     | 1 1                   | nonDrop   | continuous    |
    | smpte.xml  | 20         | smpte     | 1 1                   | nonDrop   | discontinuous |
    | smpte.xml  | 30         | smpte     | 1000 1001             | dropNTSC  | continuous    |
    | smpte.xml  | 30         | smpte     | 1000 1001             | dropNTSC  | discontinuous |
    | smpte.xml  | 30         | smpte     | 1000 1001             | dropPAL   | continuous    |
    | smpte.xml  | 30         | smpte     | 1000 1001             | dropPAL   | discontinuous |
    @skip
    | smpte.xml  | 20         | smpte     | 1 1                   |           | discontinuous |
    | smpte.xml  | 20         | smpte     | 1 1                   |           | continuous    |
    | smpte.xml  | 20         | smpte     |                       |           | discontinuous |
    | smpte.xml  | 20         | smpte     |                       |           | continuous    |
    | smpte.xml  | 20         | smpte     |                       | nonDrop   | discontinuous |
    | smpte.xml  | 20         | smpte     |                       | nonDrop   | continuous    |

  # These tests are not all passing because of the missing semantic validation piece
  Scenario: Invalid SMPTE head attributes
    Given an xml file <xml_file>
    And it has frameRate <frame_rate>
    And it has timeBase <time_base>
    And it has frameRateMultiplier <frame_rate_multiplier>
    And it has dropMode <drop_mode>
    And it has markerMode <marker_mode>
    Then document is invalid

    Examples:
    | xml_file   | frame_rate | time_base | frame_rate_multiplier | drop_mode | marker_mode   |
    | smpte.xml  | 25         | smpte     | 1 1                   | dropPAL   | other value   |
    | smpte.xml  |            | smpte     |                       |           |               |
    | smpte.xml  | 30         | smpte     | 10001001              | dropPAL   | continuous    |
    | smpte.xml  | 25         | smpte     |                       | dropPAL   | continuous    |
    | smpte.xml  | 25         | smpte     | 1 1                   |           | continuous    |
    | smpte.xml  | 25         | smpte     | 1 1                   | dropPAL   |               |
    | smpte.xml  | 25         | clock     |                       |           |               |
    | smpte.xml  |            | clock     | 1 1                   |           |               |
    | smpte.xml  |            | clock     |                       | nonDrop   |               |
    | smpte.xml  |            | clock     |                       |           |  continuous   |
    | smpte.xml  |            | clock     |                       |           | discontinuous |
    | smpte.xml  | 25         | media     |                       |           |               |
    | smpte.xml  |            | media     | 1 1                   |           |               |
    | smpte.xml  |            | media     |                       | nonDrop   |               |
    | smpte.xml  |            | media     |                       |           |  continuous   |
    | smpte.xml  |            | media     |                       |           | discontinuous |
    @skip
    | smpte.xml  |            | clock     |                       |           |               |
    | smpte.xml  |            | media     |                       |           |               |
    | smpte.xml  | 25         | smpte     | 1 1                   | dropPAL   | continuous    |
