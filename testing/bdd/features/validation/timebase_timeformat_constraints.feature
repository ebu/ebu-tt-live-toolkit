Feature: ttp:timebase-related attribute constraints
  Scenario: Valid times according to timebase
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is valid

    Examples:
    | xml_file                 | time_base | body_begin  | body_end       | body_dur     |
    | timebase_timeformat.xml  | clock     | 15.58m      | 1.5h           |              |
    | timebase_timeformat.xml  | clock     | 42:05:60.8  | 45:00:47       | 1400h        |
    | timebase_timeformat.xml  | clock     |             |                | 67ms         |
    | timebase_timeformat.xml  | clock     |             |                | 00:00:60.4   |
    | timebase_timeformat.xml  | media     | 42:05:60.8  | 45:00:47.0     |              |
    | timebase_timeformat.xml  | media     | 67.945s     | 125.0s         |              |
    | timebase_timeformat.xml  | media     | 999:09:60.8 | 1999:00:60.999 |              |
    | timebase_timeformat.xml  | media     |             |                | 99.9s        |
    | timebase_timeformat.xml  | media     |             |                | 2225:59:60.9 |


    # These tests are not all passing because the missing semantic validation piece
  @skip
  Scenario: Invalid times according to timebase
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has body duration <body_dur>
    Then document is invalid

    Examples:
    | xml_file                 | time_base | body_begin    | body_end      | body_dur      |
    | timebase_timeformat.xml  | clock     | 15.58a        | 1.5d          |               |
    | timebase_timeformat.xml  | clock     | 0142:05:60.8  | 145:00:47     |               |
    | timebase_timeformat.xml  | clock     |               |               | 199:00:60.4   |
    | timebase_timeformat.xml  | media     | 42:05:08:60.8 | 45:00:47.0    |               |
    | timebase_timeformat.xml  | media     | 67.945q       | 125.0x        |               |
    | timebase_timeformat.xml  | media     | 140:09:60.8.1 | 141:00:60.999 |               |
    | timebase_timeformat.xml  | media     |               |               | 99.9l         |
    | timebase_timeformat.xml  | media     |               |               | 225:59:60.9.3 |


  Scenario: Valid times according to timebase in p
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is valid

    Examples:
    | xml_file                 | time_base | p_begin       | p_end            |
    | timebase_timeformat.xml  | clock     | 999.99m       | 99999999.99s     |
    | timebase_timeformat.xml  | clock     | 42:05:60.8    | 45:00:47         |
    | timebase_timeformat.xml  | media     | 00.945ms      | 125.0h           |
    | timebase_timeformat.xml  | media     | 999:09:60.8   | 001000:00:60.999 |



  @skip
  Scenario: Invalid times according to timebase in p
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has p begin time <p_begin>
    And it has p end time <p_end>
    Then document is invalid

    Examples:
    | xml_file                 | time_base | p_begin       | p_end        |
    | timebase_timeformat.xml  | clock     | 099:50:05.4   |              |
    | timebase_timeformat.xml  | clock     |               | 245:45:24.54 |


  Scenario: Valid times according to timebase in span
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is valid

    Examples:
    | xml_file                 | time_base | span_begin     | span_end       |
    | timebase_timeformat.xml  | clock     | 15.00m         | 99h            |
    | timebase_timeformat.xml  | clock     | 00:05:60.8     | 45:00:47       |
    | timebase_timeformat.xml  | media     | 199.45ms       | 15s            |
    | timebase_timeformat.xml  | media     | 009900:09:60.8 | 1999:00:60.999 |



  @skip
  Scenario: Invalid times according to timebase in span
    Given an xml file <xml_file>
    And it has timeBase <time_base>
    And it has span begin time <span_begin>
    And it has span end time <span_end>
    Then document is invalid

    Examples:
    | xml_file                 | time_base | span_begin | span_end     |
    | timebase_timeformat.xml  | clock     | 205:20:19  |              |
    | timebase_timeformat.xml  | clock     |            | 045:49:00    |
