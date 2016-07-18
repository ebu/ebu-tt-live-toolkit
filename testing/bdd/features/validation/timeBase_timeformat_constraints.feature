Feature: ttp:timeBase-related attribute constraints
  Scenario: Valid times according to timeBase
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is valid

    Examples:
    | xml_file                 | time_base | body_begin  | body_end       | body_dur     |
    | timeBase_timeformat.xml  | clock     | 15.58m      | 1.5h           |              |
    | timeBase_timeformat.xml  | clock     | 42:05:60.8  | 45:00:47       | 1400h        |
    | timeBase_timeformat.xml  | clock     |             |                | 67ms         |
    | timeBase_timeformat.xml  | clock     |             |                | 00:00:60.4   |
    | timeBase_timeformat.xml  | media     | 42:05:60.8  | 45:00:47.0     |              |
    | timeBase_timeformat.xml  | media     | 67.945s     | 125.0s         |              |
    | timeBase_timeformat.xml  | media     | 999:09:60.8 | 1999:00:60.999 |              |
    | timeBase_timeformat.xml  | media     |             |                | 99.9s        |
    | timeBase_timeformat.xml  | media     |             |                | 2225:59:60.9 |
    | timeBase_timeformat.xml  | smpte     | 15:25:59:65 |                |              |
    | timeBase_timeformat.xml  | smpte     |             | 23:00:00:99    |              |


  # These tests are not all passing because the missing semantic validation piece
  Scenario: Invalid times according to timeBase
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is invalid

    Examples:
    | xml_file                 | time_base | body_begin    | body_end      | body_dur      |
    | timeBase_timeformat.xml  | clock     | 15.58a        | 1.5d          |               |
    | timeBase_timeformat.xml  | media     | 67.945q       | 125.0x        |               |
    | timeBase_timeformat.xml  | media     |               |               | 99.9l         |
    | timeBase_timeformat.xml  | media     |               |               | +12.25m       |
    | timeBase_timeformat.xml  | media     | 42:05:08:60.8 | 45:00:47.0    |               |
    | timeBase_timeformat.xml  | media     | 140:09:60.8.1 | 141:00:60.999 |               |
    | timeBase_timeformat.xml  | media     |               |               | 225:59:60.9.3 |
    | timeBase_timeformat.xml  | media     | -45ms         |               |               |
    | timeBase_timeformat.xml  | clock     | -45ms         |               |               |
    | timeBase_timeformat.xml  | smpte     | 45:25:59:65   |               |               |
    | timeBase_timeformat.xml  | smpte     |               | 23:00:70:99   |               |
    @skip 
    | timeBase_timeformat.xml  | clock     | 0142:05:60.8  | 145:00:47     |               |
    | timeBase_timeformat.xml  | clock     |               |               | 199:00:60.4   |


  # SPEC-CONFORMANCE :
  Scenario: Valid times according to timeBase in div
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is valid

    Examples:
    | xml_file                 | time_base | div_begin     | div_end          |
    | timeBase_timeformat.xml  | clock     | 999.99m       | 99999999.99s     |
    | timeBase_timeformat.xml  | clock     | 42:05:60.8    | 45:00:47         |
    | timeBase_timeformat.xml  | media     | 00.945ms      | 125.0h           |
    | timeBase_timeformat.xml  | media     | 999:09:60.8   | 001000:00:60.999 |
    | timeBase_timeformat.xml  | smpte     | 00:00:00:00   |                  |
    | timeBase_timeformat.xml  | smpte     |               | 08:59:59:99      |


  # SPEC-CONFORMANCE : R55 R56 R58 R59
  Scenario: Invalid times according to timeBase in div
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has div begin time <div_begin>
    And it has div end time <div_end>
    Then document is invalid

    Examples:
    | xml_file                 | time_base | div_begin     | div_end       |
    | timeBase_timeformat.xml  | clock     | 15.58a        | 1.5d          |
    | timeBase_timeformat.xml  | media     | 67.945q       | 125.0x        |
    | timeBase_timeformat.xml  | media     | 42:05:08:60.8 | 45:00:47.0    |
    | timeBase_timeformat.xml  | media     | 140:09:60.8.1 | 141:00:60.999 |
    | timeBase_timeformat.xml  | media     | -45ms         |               |
    | timeBase_timeformat.xml  | clock     | -45ms         |               |
    | timeBase_timeformat.xml  | smpte     | 45:25:59:65   |               |
    | timeBase_timeformat.xml  | smpte     |               | 23:00:70:99   |
    @skip
    | timeBase_timeformat.xml  | clock     | 0142:05:60.8  | 145:00:47     |
    | timeBase_timeformat.xml  | clock     |               |               |



  Scenario: Valid times according to timeBase in p
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is valid

    Examples:
    | xml_file                 | time_base | p_begin       | p_end            |
    | timeBase_timeformat.xml  | clock     | 999.99m       | 99999999.99s     |
    | timeBase_timeformat.xml  | clock     | 42:05:60.8    | 45:00:47         |
    | timeBase_timeformat.xml  | media     | 00.945ms      | 125.0h           |
    | timeBase_timeformat.xml  | media     | 999:09:60.8   | 001000:00:60.999 |
    | timeBase_timeformat.xml  | smpte     | 00:00:00:00   |                  |
    | timeBase_timeformat.xml  | smpte     |               | 08:59:59:99      |


  Scenario: Invalid times according to timeBase in p
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is invalid

    Examples:
    | xml_file                 | time_base | p_begin       | p_end         |
    | timeBase_timeformat.xml  | clock     | 15.58a        | 1.5d          |
    | timeBase_timeformat.xml  | media     | 67.945q       | 125.0x        |
    | timeBase_timeformat.xml  | media     | 42:05:08:60.8 | 45:00:47.0    |
    | timeBase_timeformat.xml  | media     | 140:09:60.8.1 | 141:00:60.999 |
    | timeBase_timeformat.xml  | media     | -45ms         |               |
    | timeBase_timeformat.xml  | clock     | -45ms         |               |
    | timeBase_timeformat.xml  | smpte     | 45:25:59:65   |               |
    | timeBase_timeformat.xml  | smpte     |               | 23:00:70:99   |
    @skip 
    | timeBase_timeformat.xml  | clock     | 0142:05:60.8  | 145:00:47     |
    | timeBase_timeformat.xml  | clock     |               |               |



  Scenario: Valid times according to timeBase in span
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is valid

    Examples:
    | xml_file                 | time_base | span_begin     | span_end       |
    | timeBase_timeformat.xml  | clock     | 15.00m         | 99h            |
    | timeBase_timeformat.xml  | clock     | 00:05:60.8     | 45:00:47       |
    | timeBase_timeformat.xml  | media     | 199.45ms       | 15s            |
    | timeBase_timeformat.xml  | media     | 009900:09:60.8 | 1999:00:60.999 |
    | timeBase_timeformat.xml  | smpte     | 00:00:00:00    |                |
    | timeBase_timeformat.xml  | smpte     |                | 08:59:59:99    |


  Scenario: Invalid times according to timeBase in span
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is invalid

    Examples:
    | xml_file                 | time_base | span_begin    | span_end      |
    | timeBase_timeformat.xml  | clock     | 15.58a        | 1.5d          |
    | timeBase_timeformat.xml  | media     | 67.945q       | 125.0x        |
    | timeBase_timeformat.xml  | media     | 42:05:08:60.8 | 45:00:47.0    |
    | timeBase_timeformat.xml  | media     | 140:09:60.8.1 | 141:00:60.999 |
    | timeBase_timeformat.xml  | media     | -45ms         |               |
    | timeBase_timeformat.xml  | clock     | -45ms         |               |
    | timeBase_timeformat.xml  | smpte     | 45:25:59:65   |               |
    | timeBase_timeformat.xml  | smpte     |               | 23:00:70:99   |
    @skip 
    | timeBase_timeformat.xml  | clock     | 0142:05:60.8  | 145:00:47     |
    | timeBase_timeformat.xml  | clock     |               |               |
