@buffer @delay
Feature: BufferDelayNode

  Examples:
  | xml_file      |
  | delayNode.xml |  


 # CONFORMANCE.md #109
  Scenario: BufferDelayNode accept non-negative value
    Given an xml file <xml_file>
    And the document is generated
    And it has availability time <avail_time>
    When the delay node delays it by <delay>
    Then the delay node outputs the document at <delayed_avail_time>

    Examples:
    | avail_time | delay      | delayed_avail_time |
    | 00:00:10.0 | 00:00:02.0 | 00:00:12.0         |
    | 00:00:10.0 | 00:00:00.0 | 00:00:10.0         |


  # CONFORMANCE.md #109, #112
  Scenario: BufferDelayNode delays emission by no less than the delay period
    Given an xml file <xml_file>
    And the document is generated
    And it has resolved begin time <resolved_begin_1>
    When the delay node delays it by <delay>
    Then the document has resolved begin time <resolved_begin_2>

    Examples:
    | resolved_begin_1 | delay      | resolved_begin_2 |  
    | 00:00:10.0       | 00:00:02.0 | 00:00:12.0       |  
    | 00:00:10.0       | 00:00:00.0 | 00:00:10.0       |  
    | 00:00:00         | 00:00:00.0 | 00:00:00.050     |


  # CONFORMANCE.md #110, #111
  Scenario: BufferDelayNode does not modify the document
  # Check that sequence identifier and timings are not changed by comparing the document as a whole
    Given an xml file <xml_file>
    And the document is generated
    And the document is hashed 
    When the delay node delays it
    Then the delayed document has the same hash 



  