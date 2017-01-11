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
    And it has availability time <avail_time>
    And the document is delayed by <delay_offset>
    And the document is emitted at <emission>
    Then the delta between <emission> and <avail_time> is greater or equal to <delay_offset>

    Examples:
    | emission   | avail_time  | delay_offset |
    | 00:00:05.0 | 00:00:02.0  | 00:00:01.0   |


  # SPEC-CONFORMANCE.md R110, R111
  Scenario: BufferDelayNode does not modify the document
  # Check that sequence identifier and timings are not changed by comparing the document as a whole
    Given an xml file <xml_file>
    And the document is generated 
    And the document has hashed value <hash_1>  
    When the delay node delays it
    Then the document has hashed value <hash_2>

    Examples:
    | hash_1                           | hash_2                           |  
    | c3f273730eada246ba9a342654f24e2a | c3f273730eada246ba9a342654f24e2a |  
