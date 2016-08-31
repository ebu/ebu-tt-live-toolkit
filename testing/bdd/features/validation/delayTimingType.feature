@validation @xsd
Feature: delayTimingType (used by attribute ebuttm:authoringDelay).
  delayTimingType is constrained to a signed (positive or negative) number with an optional decimal fraction, followed by a time metric being one of: "h" (hours), "m" (minutes), "s" (seconds),   "ms" (milliseconds).

  # SPEC-CONFORMANCE: R68
  Scenario: Invalid delayTimingType format
    Given an xml file <xml_file>
    When ebuttm:authoringDelay attribute has value <authoring_delay>
    Then document is invalid

    Examples:
    | xml_file                | authoring_delay |
    | delayTimingType.xml     | 01:00:00        |
    | delayTimingType.xml     | 01:00:00:25     |
    | delayTimingType.xml     | 125a            |


  # SPEC-CONFORMANCE: R68
  Scenario: Valid delayTimingType format
    Given an xml file <xml_file>
    When ebuttm:authoringDelay attribute has value <authoring_delay>
    Then document is valid

    Examples:
    | xml_file                | authoring_delay |
    | delayTimingType.xml     | -5h             |
    | delayTimingType.xml     | 1.5m            |
    | delayTimingType.xml     | 125s            |
    | delayTimingType.xml     | -5.4ms          |
