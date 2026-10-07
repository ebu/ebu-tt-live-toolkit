# Note: contains examples of SMPTE time base. SMPTE was removed from the specification in version 1.0. -->


@validation
Feature: ttp:referenceClockIdentifier constraints testing
  Scenario Outline: Valid use of referenceClockIdentifier
    Given an xml file "referenceClockIdentifier.xml"
    When it has timeBase <time_base>
    And it has clock mode <clock_mode>
    And it has reference clock identifier <ref_clock_id>
    Then document is valid

    Examples:
    | time_base | clock_mode | ref_clock_id         |
    | clock     | local      | http://test.com      |
    | clock     | utc        |                      |
    | clock     | gps        |                      |
    | media     |            |                      |
    | smpte     |            | ../clock/clock.clock |
    | clock     | local      |                      |
    | smpte     |            |                      |


  @skip
  Scenario Outline: Invalid use of referenceClockIdentifier
    Given an xml file "referenceClockIdentifier.xml"
    When it has timeBase <time_base>
    And it has clock mode <clock_mode>
    And it has reference clock identifier <ref_clock_id>
    Then document is invalid

    Examples:
    | time_base | clock_mode | ref_clock_id    |
    | clock     | utc        | http://test.com |
    | clock     | gps        | http://test.com |
    | media     |            | http://test.com |
