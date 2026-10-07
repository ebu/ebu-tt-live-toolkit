# Note: contains examples of SMPTE time base. SMPTE was removed from the specification in version 1.0. -->


# SPEC-CONFORMANCE : R70
@validation @xsd @syntax @times
Feature: ttp:timeBase-related attribute constraints

  # SPEC-CONFORMANCE: R45 R46 R47 R48 R49 R50 R51 R52 R53
  Scenario Outline: Valid times according to timeBase in body
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is valid

    Examples:
    | time_base | body_begin  | body_end       | body_dur     |
    | clock     | 15.58m      | 1.5h           |              |
    | clock     | 42:05:60.8  | 45:00:47       | 1400h        |
    | clock     |             |                | 67ms         |
    | clock     |             |                | 00:00:60.4   |
    | media     | 42:05:60.8  | 45:00:47.0     |              |
    | media     | 67.945s     | 125.0s         |              |
    | media     | 999:09:60.8 | 1999:00:60.999 |              |
    | media     |             |                | 99.9s        |
    | media     |             |                | 2225:59:60.9 |
    | smpte     | 00:00:00:00 |                |              |
    | smpte     | 11:11:11:11 | 11:11:11:12    |              |
    | smpte     | 11:11:11:11 | 11:11:11:12    |              |


  # These tests are not all passing because the missing semantic validation piece
  # SPEC-CONFORMANCE: R46 R47 R49 R50 R52 R53
  Scenario Outline: Invalid times according to timeBase in body
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is invalid

    Examples:
    | time_base | body_begin    | body_end      | body_dur      |
    | clock     | 15.58a        | 1.5d          |               |
    | media     | 67.945q       | -125.0x       |               |
    | media     |               |               | 99.9l         |
    | media     | 42:05:08:60.8 | 45:00:47.0    |               |
    | media     | 140:09:60.8.1 | 141:00:60.999 |               |
    | media     |               |               | 225:59:60.9.3 |
    | clock     | 0142:05:60.8  | 145:00:47     |               |
    | clock     |               |               | 199:00:60.4   |
    | smpte     | 00:00:00      |               |               |
    | smpte     | 11            |               |               |
    | smpte     | 11:11.11      |               |               |
    | smpte     | 11.11.11      |               |               |
    | smpte     | 11.11:11      |               |               |
    | smpte     | 11.11         |               |               |
    | smpte     | 11:11:11:111  |               |               |



  # SPEC-CONFORMANCE: R55 R56 R58 R59
  Scenario Outline: Valid times according to timeBase in div
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is valid

    Examples:
    | time_base | div_begin    | div_end        |
    | clock     | 15.58m       | 1.5h           |
    | clock     | 42:05:60.8   | 45:00:47       |
    | media     | 42:05:60.8   | 45:00:47.0     |
    | media     | 67.945s      | 125.0s         |
    | media     | 999:09:60.8  | 1999:00:60.999 |
    | clock     | 45:00:47     | 1400h          |
    | clock     | 1400h        |                |
    | clock     | 00:00:60.4   |                |
    | media     | 42:05:60.8   | 45:00:47.0     |
    | media     | 67.945s      | 125.0s         |
    | media     | 999:09:60.8  | 1999:00:60.999 |
    | media     | 99.9s        |                |
    | media     | 2225:59:60.9 |                |
    | media     | 42:05:60.8   | 45:00:47.0     |
    | media     | 67.945s      | 125.0s         |
    | media     | 999:09:60.8  | 1999:00:60.999 |
    | media     | 99.9s        |                |
    | media     | 2225:59:60.9 |                |
    | smpte     | 00:00:00:00  |                |
    | smpte     | 11:11:11:11  | 11:11:11:12    |
    | smpte     | 11:11:11:11  | 11:11:11:12    |


  Scenario Outline: Invalid times according to timeBase in div
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is invalid

    Examples:
    | time_base | div_begin     | div_end       |
    | clock     | 15.58a        | 1.5d          |
    | media     | 67.945q       | -125.0x       |
    | media     | 99.9l         |               |
    | media     | 42:05:08:60.8 | 45:00:47.0    |
    | media     | 140:09:60.8.1 | 141:00:60.999 |
    | media     | 225:59:60.9.3 |               |
    | clock     | 0142:05:60.8  | 145:00:47     |
    | clock     | 199:00:60.4   |               |
    | smpte     | 11            |               |
    | smpte     | 11:11.11      |               |
    | smpte     | 11.11.11      |               |
    | smpte     | 11.11:11      |               |
    | smpte     | 11.11         |               |
    | smpte     | 11:11:11:111  |               |


  # SPEC-CONFORMANCE: R60 R61 R63 R62 R64 R65
  Scenario Outline: Valid times according to timeBase in p
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is valid

    Examples:
    | time_base | p_begin     | p_end            |
    | clock     | 999.99m     | 99999999.99s     |
    | clock     | 42:05:60.8  | 45:00:47         |
    | media     | 00.945ms    | 125.0h           |
    | media     | 999:09:60.8 | 001000:00:60.999 |
    | smpte     | 00:00:00:00 |                  |
    | smpte     | 11:11:11:11 | 11:11:11:12      |
    | smpte     | 11:11:11:11 | 11:11:11:12      |


  # SPEC-CONFORMANCE: R61 R62 R64 R65
  Scenario Outline: Invalid times according to timeBase in p
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is invalid

    Examples:
    | time_base | p_begin      | p_end        |
    | clock     | 099:50:05.4  |              |
    | clock     |              | 245:45:24.54 |
    | smpte     | 00:00:00     |              |
    | smpte     | 11           |              |
    | smpte     | 11:11.11     |              |
    | smpte     | 11.11.11     |              |
    | smpte     | 11.11:11     |              |
    | smpte     | 11.11        |              |
    | smpte     | 11:11:11:111 |              |

  # SPEC-CONFORMANCE: R101 R102 R103 R104 R105 R106
  Scenario Outline: Valid times according to timeBase in span
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is valid

    Examples:
    | time_base | span_begin     | span_end       |
    | clock     | 15.00m         | 99h            |
    | clock     | 00:05:60.8     | 45:00:47       |
    | media     | 199.45ms       | 15s            |
    | media     | 009900:09:60.8 | 1999:00:60.999 |
    | smpte     | 00:00:00:00    |                |
    | smpte     | 11:11:11:11    | 11:11:11:12    |
    | smpte     | 11:11:11:11    | 11:11:11:12    |


  Scenario Outline: Invalid times according to timeBase in span
    Given an xml file "timeBase_timeformat.xml"
    When it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is invalid

    Examples:
    | time_base | span_begin   | span_end  |
    | clock     | 205:20:19    |           |
    | clock     |              | 045:49:00 |
    | smpte     | 00:00:00     |           |
    | smpte     | 11           |           |
    | smpte     | 11:11.11     |           |
    | smpte     | 11.11.11     |           |
    | smpte     | 11.11:11     |           |
    | smpte     | 11.11        |           |
    | smpte     | 11:11:11:111 |           |

Scenario Outline: Times in documentStartOfProgramme do not cause processing or validation error
  Given an xml file "timeBase_timeformat.xml"
  When it has timeBase <time_base>
  And it has documentStartOfProgramme <start_time>
  Then document is valid

  Examples:
  | time_base  | start_time   |
  | media      | 00:00:00.000 |
  | clock      | 00:00:00.000 |
  | smpte      | 10:00:00:00  |

# Element based time validation is not yet implemented
@skip
Scenario Outline: Times in documentStartOfProgramme do cause validation error
  Given an xml file "timeBase_timeformat.xml"
  When it has timeBase <time_base>
  And it has documentStartOfProgramme <start_time>
  Then document is invalid

  Examples:
  | time_base  | start_time   |
  | media      | 00:00:00:00  |
  | clock      | 00:00:60     |
  | smpte      | 10:00:00.00  |
