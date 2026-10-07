@validation @xsd
Feature: delayTimingType (used by attribute ebuttm:authoringDelay).
  delayTimingType is constrained to a signed (positive or negative) number with an optional decimal fraction, followed by a time metric being one of: "h" (hours), "m" (minutes), "s" (seconds),   "ms" (milliseconds).

  # SPEC-CONFORMANCE: R68
  Scenario Outline: Invalid delayTimingType format
    Given an xml file "delayTimingType.xml"
    When ebuttm:authoringDelay attribute has value <authoring_delay>
    Then document is invalid

    Examples:
    | authoring_delay |
    | 01:00:00        |
    | 01:00:00:25     |
    | 125a            |


  # SPEC-CONFORMANCE: R68
  Scenario Outline: Valid delayTimingType format
    Given an xml file "delayTimingType.xml"
    When ebuttm:authoringDelay attribute has value <authoring_delay>
    Then document is valid

    Examples:
    | authoring_delay |
    | -5h             |
    | 1.5m            |
    | 125s            |
    | -5.4ms          |
