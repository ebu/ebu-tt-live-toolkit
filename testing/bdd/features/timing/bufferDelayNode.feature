@buffer @delay
Feature: BufferDelayNode

  Examples:
  | xml_file      |
  | delayNode.xml |  

  # SPEC-CONFORMANCE.md R109, R112
  # Any delay introduced by the carriage mechanism can not lead to a test passing falsely. 
  # For example, if the desired delay offset is 10s and the carriage mech imposes a delay of 3s, 
  # then an actual delay in the range 7s -> 10s would lead to the test passing because the 3s of 
  # carriage delay would be added. This would not be correct.
  # BufferDelay.emission_time - BufferDelay.availability_time >= delay_offset

  Scenario: BufferDelayNode delays emission by no less than the delay period
    Given an xml file <xml_file>
    And the document is generated
    And the document has availability time <availability_1>  
    And the document is delayed by <delay_offset>
    And the document is emitted at <emission>
    And the document has availability time <availability_2>
    Then the delta between emission and availability_1 is greater or equal to <delay_offset>


  # SPEC-CONFORMANCE.md R110, R111
  Scenario: BufferDelayNode does not modify the document
  # Check that sequence identifier and timings are not changed by comparing the document as a whole
    Given an xml file <xml_file>
    And the document is generated 
    And the document is hashed 
    When the delay node delays it
    And the document is hashed
    Then the hash is identical



  