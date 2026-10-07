@validation @syntax @metadata
Feature: Applied processing element constrainst
  Attributes `process` and `generatedBy` are mandatory.

  # SPEC-CONFORMANCE : R31 R42 R43
  Scenario Outline: Invalid applied processing attributes
    Given an xml file "applied-processing.xml"
    When appliedProcessing element has process attribute <process>
    And appliedProcessing element has generatedBy attribute <generated_by>
    And appliedProcessing element has sourceId attribute <source_id>
    Then document is invalid

    Examples:
    | process  | generated_by | source_id       |
    |          | producer.py  |                 |
    | creation |              |                 |
    |          |              | lorem_ipsum.txt |


Scenario Outline: Valid applied process attributes
    Given an xml file "applied-processing.xml"
    When appliedProcessing element has process attribute <process>
    And appliedProcessing element has generatedBy attribute <generated_by>
    And appliedProcessing element has sourceId attribute <source_id>
    Then document is valid

    Examples:
    | process    | generated_by | source_id       |
    | creation   | producer.py  | lorem_ipsum.txt |
    | validation | producer.py  |                 |
