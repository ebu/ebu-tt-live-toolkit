# Note: contains examples of SMPTE time base. SMPTE was removed from the specification in version 1.0. -->


# SPEC-CONFORMANCE : R70
@validation @xsd @syntax @times
Feature: ttp:timeBase-related attribute constraints

  # SPEC-CONFORMANCE: R45 R46 R47 R48 R49 R50 R51 R52 R53
  Scenario: Valid times according to timeBase in body
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is valid

    Examples:
    | xml_file                | time_base | body_begin  | body_end       | body_dur     |
    | timeBase_timeformat.xml | clock     | 15.58m      | 1.5h           |              |
    | timeBase_timeformat.xml | clock     | 42:05:60.8  | 45:00:47       | 1400h        |
    | timeBase_timeformat.xml | clock     |             |                | 67ms         |
    | timeBase_timeformat.xml | clock     |             |                | 00:00:60.4   |
    | timeBase_timeformat.xml | media     | 42:05:60.8  | 45:00:47.0     |              |
    | timeBase_timeformat.xml | media     | 67.945s     | 125.0s         |              |
    | timeBase_timeformat.xml | media     | 999:09:60.8 | 1999:00:60.999 |              |
    | timeBase_timeformat.xml | media     |             |                | 99.9s        |
    | timeBase_timeformat.xml | media     |             |                | 2225:59:60.9 |
    | timeBase_timeformat.xml | smpte     | 00:00:00:00 |                |              |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12    |              |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12    |              |


  # These tests are not all passing because the missing semantic validation piece
  # SPEC-CONFORMANCE: R46 R47 R49 R50 R52 R53
  Scenario: Invalid times according to timeBase in body
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is invalid

    Examples:
    | xml_file                | time_base | body_begin    | body_end      | body_dur      |
    | timeBase_timeformat.xml | clock     | 15.58a        | 1.5d          |               |
    | timeBase_timeformat.xml | media     | 67.945q       | -125.0x       |               |
    | timeBase_timeformat.xml | media     |               |               | 99.9l         |
    | timeBase_timeformat.xml | media     | 42:05:08:60.8 | 45:00:47.0    |               |
    | timeBase_timeformat.xml | media     | 140:09:60.8.1 | 141:00:60.999 |               |
    | timeBase_timeformat.xml | media     |               |               | 225:59:60.9.3 |
    | timeBase_timeformat.xml | clock     | 0142:05:60.8  | 145:00:47     |               |
    | timeBase_timeformat.xml | clock     |               |               | 199:00:60.4   |
    | timeBase_timeformat.xml | smpte     | 00:00:00      |               |               |
    | timeBase_timeformat.xml | smpte     | 11            |               |               |
    | timeBase_timeformat.xml | smpte     | 11:11.11      |               |               |
    | timeBase_timeformat.xml | smpte     | 11.11.11      |               |               |
    | timeBase_timeformat.xml | smpte     | 11.11:11      |               |               |
    | timeBase_timeformat.xml | smpte     | 11.11         |               |               |
    | timeBase_timeformat.xml | smpte     | 11:11:11:111  |               |               |



  # SPEC-CONFORMANCE: R55 R56 R58 R59
  Scenario: Valid times according to timeBase in div
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is valid

    Examples:
    | xml_file                | time_base | div_begin    | div_end        |
    | timeBase_timeformat.xml | clock     | 15.58m       | 1.5h           |
    | timeBase_timeformat.xml | clock     | 42:05:60.8   | 45:00:47       |
    | timeBase_timeformat.xml | media     | 42:05:60.8   | 45:00:47.0     |
    | timeBase_timeformat.xml | media     | 67.945s      | 125.0s         |
    | timeBase_timeformat.xml | media     | 999:09:60.8  | 1999:00:60.999 |
    | timeBase_timeformat.xml | clock     | 45:00:47     | 1400h          |
    | timeBase_timeformat.xml | clock     | 1400h        |                |
    | timeBase_timeformat.xml | clock     | 00:00:60.4   |                |
    | timeBase_timeformat.xml | media     | 42:05:60.8   | 45:00:47.0     |
    | timeBase_timeformat.xml | media     | 67.945s      | 125.0s         |
    | timeBase_timeformat.xml | media     | 999:09:60.8  | 1999:00:60.999 |
    | timeBase_timeformat.xml | media     | 99.9s        |                |
    | timeBase_timeformat.xml | media     | 2225:59:60.9 |                |
    | timeBase_timeformat.xml | media     | 42:05:60.8   | 45:00:47.0     |
    | timeBase_timeformat.xml | media     | 67.945s      | 125.0s         |
    | timeBase_timeformat.xml | media     | 999:09:60.8  | 1999:00:60.999 |
    | timeBase_timeformat.xml | media     | 99.9s        |                |
    | timeBase_timeformat.xml | media     | 2225:59:60.9 |                |
    | timeBase_timeformat.xml | smpte     | 00:00:00:00  |                |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11  | 11:11:11:12    |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11  | 11:11:11:12    |


  Scenario: Invalid times according to timeBase in div
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is invalid

    Examples:
    | xml_file                | time_base | div_begin     | div_end       |
    | timeBase_timeformat.xml | clock     | 15.58a        | 1.5d          |
    | timeBase_timeformat.xml | media     | 67.945q       | -125.0x       |
    | timeBase_timeformat.xml | media     | 99.9l         |               |
    | timeBase_timeformat.xml | media     | 42:05:08:60.8 | 45:00:47.0    |
    | timeBase_timeformat.xml | media     | 140:09:60.8.1 | 141:00:60.999 |
    | timeBase_timeformat.xml | media     | 225:59:60.9.3 |               |
    | timeBase_timeformat.xml | clock     | 0142:05:60.8  | 145:00:47     |
    | timeBase_timeformat.xml | clock     | 199:00:60.4   |               |
    | timeBase_timeformat.xml | smpte     | 11            |               |
    | timeBase_timeformat.xml | smpte     | 11:11.11      |               |
    | timeBase_timeformat.xml | smpte     | 11.11.11      |               |
    | timeBase_timeformat.xml | smpte     | 11.11:11      |               |
    | timeBase_timeformat.xml | smpte     | 11.11         |               |
    | timeBase_timeformat.xml | smpte     | 11:11:11:111  |               |


  # SPEC-CONFORMANCE: R60 R61 R63 R62 R64 R65
  Scenario: Valid times according to timeBase in p
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is valid

    Examples:
    | xml_file                | time_base | p_begin     | p_end            |
    | timeBase_timeformat.xml | clock     | 999.99m     | 99999999.99s     |
    | timeBase_timeformat.xml | clock     | 42:05:60.8  | 45:00:47         |
    | timeBase_timeformat.xml | media     | 00.945ms    | 125.0h           |
    | timeBase_timeformat.xml | media     | 999:09:60.8 | 001000:00:60.999 |
    | timeBase_timeformat.xml | smpte     | 00:00:00:00 |                  |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12      |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11 | 11:11:11:12      |


  # SPEC-CONFORMANCE: R61 R62 R64 R65
  Scenario: Invalid times according to timeBase in p
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is invalid

    Examples:
    | xml_file                | time_base | p_begin      | p_end        |
    | timeBase_timeformat.xml | clock     | 099:50:05.4  |              |
    | timeBase_timeformat.xml | clock     |              | 245:45:24.54 |
    | timeBase_timeformat.xml | smpte     | 00:00:00     |              |
    | timeBase_timeformat.xml | smpte     | 11           |              |
    | timeBase_timeformat.xml | smpte     | 11:11.11     |              |
    | timeBase_timeformat.xml | smpte     | 11.11.11     |              |
    | timeBase_timeformat.xml | smpte     | 11.11:11     |              |
    | timeBase_timeformat.xml | smpte     | 11.11        |              |
    | timeBase_timeformat.xml | smpte     | 11:11:11:111 |              |

  # SPEC-CONFORMANCE: R101 R102 R103 R104 R105 R106
  Scenario: Valid times according to timeBase in span
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is valid

    Examples:
    | xml_file                | time_base | span_begin     | span_end       |
    | timeBase_timeformat.xml | clock     | 15.00m         | 99h            |
    | timeBase_timeformat.xml | clock     | 00:05:60.8     | 45:00:47       |
    | timeBase_timeformat.xml | media     | 199.45ms       | 15s            |
    | timeBase_timeformat.xml | media     | 009900:09:60.8 | 1999:00:60.999 |
    | timeBase_timeformat.xml | smpte     | 00:00:00:00    |                |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11    | 11:11:11:12    |
    | timeBase_timeformat.xml | smpte     | 11:11:11:11    | 11:11:11:12    |


  Scenario: Invalid times according to timeBase in span
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is invalid

    Examples:
    | xml_file                | time_base | span_begin   | span_end  |
    | timeBase_timeformat.xml | clock     | 205:20:19    |           |
    | timeBase_timeformat.xml | clock     |              | 045:49:00 |
    | timeBase_timeformat.xml | smpte     | 00:00:00     |           |
    | timeBase_timeformat.xml | smpte     | 11           |           |
    | timeBase_timeformat.xml | smpte     | 11:11.11     |           |
    | timeBase_timeformat.xml | smpte     | 11.11.11     |           |
    | timeBase_timeformat.xml | smpte     | 11.11:11     |           |
    | timeBase_timeformat.xml | smpte     | 11.11        |           |
    | timeBase_timeformat.xml | smpte     | 11:11:11:111 |           |

Scenario: Times in documentStartOfProgramme do not cause processing or validation error
  Given an xml file <xml_file>
  When it has timeBase <time_base>
  And it has documentStartOfProgramme <start_time>
  Then document is valid

  Examples:
  | xml_file                        | time_base  | start_time   |
  | timeBase_timeformat.xml         | media      | 00:00:00.000 |
  | timeBase_timeformat.xml         | clock      | 00:00:00.000 |
  | timeBase_timeformat.xml         | smpte      | 10:00:00:00  |

# Element based time validation is not yet implemented
@skip
Scenario: Times in documentStartOfProgramme do cause validation error
  Given an xml file <xml_file>
  When it has timeBase <time_base>
  And it has documentStartOfProgramme <start_time>
  Then document is invalid

  Examples:
  | xml_file                        | time_base  | start_time   |
  | timeBase_timeformat.xml         | media      | 00:00:00:00  |
  | timeBase_timeformat.xml         | clock      | 00:00:60     |
  | timeBase_timeformat.xml         | smpte      | 10:00:00.00  |
