@timing @delay
Feature: Delay of a document sequence

  Examples:
  | xml_file      |
  | delayNode.xml |

  @skip
  Scenario: Implicitly timed document
    Given an xml file <xml_file>
    And the document is generated
    And it has availability time <avail_time>
    When the delay node delays it by <delay>
    Then the delay node outputs the document at <delayed_avail_time>

  Examples:
  | avail_time | delay      | delayed_avail_time |
  | 00:00:10.0 | 00:00:02.0 | 00:00:12.0         |

  Scenario: Explicitly timed document
    Given an xml file <xml_file>
    And the document is generated
    And it has body begin time <body_begin>
    And it has body end time <body_end>
    And it has div begin time <div_begin>
    And it has p begin time <p_begin>
    When the delay node delays it by <delay>
    Then the updated body begin time is <updated_body_begin>
    Then the updated body end time is <updated_body_end>
    Then the updated div begin time is <updated_div_begin>
    Then the updated p begin time is <updated_p_begin>

  Examples:
  | delay    | body_begin   | updated_body_begin | body_end     | updated_body_end | div_begin | updated_div_begin | p_begin  | updated_p_begin |
  | 00:00:02 | 00:00:00.500 | 00:00:02.500       | 00:00:02     | 00:00:04         | 00:00:03  | 00:00:03          | 00:00:05 | 00:00:05        |
  | 00:00:02 |              |                    | 00:00:02     | 00:00:04         | 00:00:03  | 00:00:05          | 00:00:05 | 00:00:05        |
  | 00:00:02 |              |                    |              |                  |           |                   | 00:00:05 | 00:00:07        |
