@validation 
Feature: ttp:referenceClockIdentifier constraints testing
  Scenario: Valid use of referenceClockIdentifier
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has clock mode <clock_mode>
    And it has reference clock identifier <ref_clock_id>
    Then document is valid

    Examples:
    | xml_file                      | time_base | clock_mode | ref_clock_id         |
    | referenceClockIdentifier.xml  | clock     | local      | http://test.com      |
    | referenceClockIdentifier.xml  | clock     | utc        |                      |
    | referenceClockIdentifier.xml  | clock     | gps        |                      |
    | referenceClockIdentifier.xml  | media     |            |                      |
    | referenceClockIdentifier.xml  | smpte     |            | ../clock/clock.clock |
    | referenceClockIdentifier.xml  | clock     | local      |                      |
    | referenceClockIdentifier.xml  | smpte     |            |                      |


  @skip
  Scenario: Invalid use of referenceClockIdentifier
    Given an xml file <xml_file>
    When it has timeBase <time_base>
    And it has clock mode <clock_mode>
    And it has reference clock identifier <ref_clock_id>
    Then document is invalid

    Examples:
    | xml_file                      | time_base | clock_mode | ref_clock_id    |
    | referenceClockIdentifier.xml  | clock     | utc        | http://test.com |
    | referenceClockIdentifier.xml  | clock     | gps        | http://test.com |
    | referenceClockIdentifier.xml  | media     |            | http://test.com |
