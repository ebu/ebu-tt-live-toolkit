# SPEC-CONFORMANCE.md : R71 R72 R73a R96
@validation @smpte
Feature: SMPTE-related attribute constraints
  Scenario: Valid SMPTE head attributes
    Given an xml file <xml_file>
    When it has frameRate <frame_rate>
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
    | smpte.xml  | 25         | clock     |                       |           |               |
    | smpte.xml  |            | clock     | 1 1                   |           |               |
    | smpte.xml  | 25         | media     |                       |           |               |
    | smpte.xml  |            | media     | 1 1                   |           |               |
    | smpte.xml  |            | clock     |                       |           |               |
    | smpte.xml  |            | media     |                       |           |               |
    @skip
    | smpte.xml  | 20         | smpte     |                       | nonDrop   | discontinuous |
    | smpte.xml  | 20         | smpte     |                       | nonDrop   | continuous    |

  # These tests are not all passing because of the missing semantic validation described in #52
  Scenario: Invalid SMPTE head attributes
    Given an xml file <xml_file>
    When it has frameRate <frame_rate>
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
    | smpte.xml  | 25         | smpte     | 1 1                   |           | continuous    |
    | smpte.xml  | 25         | smpte     | 1 1                   | nonDrop   |               |
    | smpte.xml  |            | clock     |                       | nonDrop   |               |
    | smpte.xml  |            | clock     |                       |           |  continuous   |
    | smpte.xml  |            | clock     |                       |           | discontinuous |
    | smpte.xml  |            | media     |                       | nonDrop   |               |
    | smpte.xml  |            | media     |                       |           |  continuous   |
    | smpte.xml  |            | media     |                       |           | discontinuous |
    | smpte.xml  |            | smpte     | 1 1                   | nonDrop   | continuous    |
    | smpte.xml  | 25         | smpte     | 1.5 1                 | nonDrop   | continuous    |
    | smpte.xml  | 25         | smpte     | -1 1                  | nonDrop   | continuous    |
    @skip
    # dropPAL and 1 1 doesn't work together
    | smpte.xml  | 25         | smpte     | 1 1                   | dropPAL   | continuous    |
    # default value of frame rate multiplier
    | smpte.xml  | 25         | smpte     |                       | dropPAL   | continuous    |
