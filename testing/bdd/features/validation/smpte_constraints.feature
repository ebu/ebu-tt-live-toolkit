# Note: contains legacy scenarios for SMPTE time base. SMPTE was removed from the specification in version 1.0. -->


# SPEC-CONFORMANCE.md : R71 R72 R73a R96
@validation @smpte
Feature: SMPTE-related attribute constraints
  Scenario Outline: Valid SMPTE head attributes
    Given an xml file "smpte.xml"
    When it has frameRate <frame_rate>
    And it has timeBase <time_base>
    And it has frameRateMultiplier <frame_rate_multiplier>
    And it has dropMode <drop_mode>
    And it has markerMode <marker_mode>
    Then document is valid

    Examples:
    | frame_rate | time_base | frame_rate_multiplier | drop_mode | marker_mode   |
    | 25         | smpte     | 1 1                   | nonDrop   | continuous    |
    | 20         | smpte     | 1 1                   | nonDrop   | discontinuous |
    | 30         | smpte     | 1000 1001             | dropNTSC  | continuous    |
    | 30         | smpte     | 1000 1001             | dropNTSC  | discontinuous |
    | 30         | smpte     | 1000 1001             | dropPAL   | continuous    |
    | 30         | smpte     | 1000 1001             | dropPAL   | discontinuous |
    | 25         | clock     |                       |           |               |
    |            | clock     | 1 1                   |           |               |
    | 25         | media     |                       |           |               |
    |            | media     | 1 1                   |           |               |
    |            | clock     |                       |           |               |
    |            | media     |                       |           |               |
    # @skip
    # | 20         | smpte     |                       | nonDrop   | discontinuous |
    # | 20         | smpte     |                       | nonDrop   | continuous    |

  # These tests are not all passing because of the missing semantic validation described in #52
  Scenario Outline: Invalid SMPTE head attributes
    Given an xml file "smpte.xml"
    When it has frameRate <frame_rate>
    And it has timeBase <time_base>
    And it has frameRateMultiplier <frame_rate_multiplier>
    And it has dropMode <drop_mode>
    And it has markerMode <marker_mode>
    Then document is invalid

    Examples:
    | frame_rate | time_base | frame_rate_multiplier | drop_mode | marker_mode   |
    | 25         | smpte     | 1 1                   | dropPAL   | other value   |
    |            | smpte     |                       |           |               |
    | 30         | smpte     | 10001001              | dropPAL   | continuous    |
    | 25         | smpte     | 1 1                   |           | continuous    |
    | 25         | smpte     | 1 1                   | nonDrop   |               |
    |            | clock     |                       | nonDrop   |               |
    |            | clock     |                       |           |  continuous   |
    |            | clock     |                       |           | discontinuous |
    |            | media     |                       | nonDrop   |               |
    |            | media     |                       |           |  continuous   |
    |            | media     |                       |           | discontinuous |
    |            | smpte     | 1 1                   | nonDrop   | continuous    |
    | 25         | smpte     | 1.5 1                 | nonDrop   | continuous    |
    | 25         | smpte     | -1 1                  | nonDrop   | continuous    |
    # @skip
    # dropPAL and 1 1 doesn't work together
    # | 25         | smpte     | 1 1                   | dropPAL   | continuous    |
    # default value of frame rate multiplier
    # | 25         | smpte     |                       | dropPAL   | continuous    |
