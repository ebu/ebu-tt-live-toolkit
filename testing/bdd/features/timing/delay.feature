@timing
Feature: Delay of a document sequence

  Examples:
  | xml_file            |
  | delayTimingType.xml |

  Scenario: Implicitly timed document
    Given an xml file <xml_file>
    And it has availability time <avail_time>
    When the delay is <delay>
    Then the delay node outputs the document at <delayed_avail_time>

  Examples:
  | avail_time | delay      | delayed_avail_time |
  | 00:00:10.0 | 00:00:2.0  | 00:00:12.0