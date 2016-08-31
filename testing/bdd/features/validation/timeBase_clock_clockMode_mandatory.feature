@validation @syntax @xsd
Feature: clockMode attribute is mandatory when timeBase="clock"

  Examples:
  | xml_file                               |
  | timeBase_clock_clockMode_mandatory.xml |

  # SPEC-CONFORMANCE: R73b
  Scenario: Valid ttp:clockMode
    Given an xml file <xml_file>
    When it has ttp:timeBase attribute <time_base>
    And it has ttp:clockMode attribute <clock_mode>
    Then document is valid

    Examples:
    | time_base | clock_mode    |
    | clock     | local         |
    | clock     | utc           |
    | clock     | gps           |


  # SPEC-CONFORMANCE: R73b
  Scenario: Invalid ttp:clockMode
    Given an xml file <xml_file>
    When it has ttp:timeBase attribute <time_base>
    And it has ttp:clockMode attribute <clock_mode>
    Then document is invalid

    Examples:
    | time_base | clock_mode    |
    | clock     |               |
    | clock     | *?Empty?*     |
    | clock     | other         |
