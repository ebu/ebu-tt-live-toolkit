@buffer @delay
Feature: BufferDelayNode

  Examples:
  | xml_file      |
  | delayNode.xml |  

  # SPEC-CONFORMANCE.md R109, R112
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
    # No latency other than delay
    | 00:00:00   | 00:00:00         | 00:00:02   | 00:00:02     | 00:00:02         |  
    # Added carriage and processing latency
    | 00:00:00.0 | 00:00:00.050     | 00:00:02.0 | 00:00:02.075 | 00:00:02.100     |  


  # SPEC-CONFORMANCE.md R110, R111
  Scenario: BufferDelayNode does not modify the document
  # Check that sequence identifier and timings are not changed by comparing the document as a whole
    Given an xml file <xml_file>
    And the document is generated 
    And the document is hashed 
    When the delay node delays it
    And the document is hashed
    Then the hash is identical



  