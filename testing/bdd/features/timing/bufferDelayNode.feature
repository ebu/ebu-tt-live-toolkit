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
  # Producer Node -> Consumer Node A -> BufferDelay Node -> Consumer Node B. 
  # Difference between resolved document begin times logged by A and B should be equal or greater to delay period.

  Scenario: BufferDelayNode delays emission by no less than the delay period
    Given an xml file <xml_file>
    And the document is emitted at <emission_1>
    And the document is consumed with resolved begin time <resolved_begin_1>
    When the document is delayed by <delay>
    And the document is emitted at <emission_2>
    Then the the document is consumed with resolved begin time <resolved_begin_2>

    Examples:
    | emission_1 | resolved_begin_1 | delay      | emission_2   | resolved_begin_2 |  
    # Added carriage and processing delay
    | 00:00:00.0 | 00:00:00.050     | 00:00:02.0 | 00:00:02.050 | 00:00:02.075     |  


  # CONFORMANCE.md #110, #111
  Scenario: BufferDelayNode does not modify the document
  # Check that sequence identifier and timings are not changed by comparing the document as a whole
    Given an xml file <xml_file>
    And the document is generated 
    And the document is hashed 
    When the delay node delays it
    Then the delayed document has the same hash



  