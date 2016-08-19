@times @validation @parse_times
Feature: Regex parsing TimecountTimingType values
  # Regex for other time types are inderectly checked by 

  # SPEC-CONFORMANCE:
  Scenario: Valid times according to timeBase
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has body begin time <body_begin>
    Then timedelta value given when reading body.begin should be <trusted_timedeltas_index>
    # The trusted array of timedeltas is defined in test_time_regex_parsing.py. Best way found to check
    # the correctness of the parsing.

    Examples:
    | xml_file                | time_base | body_begin    | trusted_timedeltas_index |
    | time_regex_parsing.xml  | clock     | 15h           | 0                        |
    | time_regex_parsing.xml  | clock     | 30m           | 1                        |
    | time_regex_parsing.xml  | clock     | 42s           | 2                        |
    | time_regex_parsing.xml  | clock     | 67ms          | 3                        |
    | time_regex_parsing.xml  | clock     | 42:05:60.234  | 4                        |
    | time_regex_parsing.xml  | media     | 999:09:60.005 | 5                        |
