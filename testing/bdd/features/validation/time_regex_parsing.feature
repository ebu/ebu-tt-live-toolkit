@times @validation @parse_times
Feature: Regex parsing TimecountTimingType values
  # Regex for other time types are inderectly checked by

  # SPEC-CONFORMANCE:
  Scenario Outline: Valid times according to timeBase
    Given an xml file "time_regex_parsing.xml"
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    Then timedelta value given when reading body.begin should be <h> <m> <s> <ms>

    Examples:
    | time_base | body_begin    | h   | m  | s  | ms  |
    | clock     | 15h           |  15 |  0 |  0 |   0 |
    | clock     | 30m           |   0 | 30 |  0 |   0 |
    | clock     | 42s           |   0 |  0 | 42 |   0 |
    | clock     | 67ms          |   0 |  0 |  0 |  67 |
    | clock     | 42:05:60.234  |  42 |  5 | 60 | 234 |
    | media     | 999:09:60.005 | 999 |  9 | 60 |   5 |

