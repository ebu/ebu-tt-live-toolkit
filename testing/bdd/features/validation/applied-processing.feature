@validation @syntax @metadata
Feature: Applied processing element constrainst
  Attributes `process` and `generatedBy` are mandatory.

  # SPEC-CONFORMANCE : R31 R42 R43
  Scenario: Invalid applied processing attributes
    Given an xml file <xml_file>
    When trace element has process attribute <process>
    And trace element has generatedBy attribute <generated_by>
    And trace element has sourceId attribute <source_id>
    Then document is invalid

    Examples:
    | xml_file               | process  | generated_by | source_id       |
    | applied-processing.xml |          | producer.py  |                 |
    | applied-processing.xml | creation |              |                 |
    | applied-processing.xml |          |              | lorem_ipsum.txt |


Scenario: Valid applied process attributes
    Given an xml file <xml_file>
    When trace element has process attribute <process>
    And trace element has generatedBy attribute <generated_by>
    And trace element has sourceId attribute <source_id>
    Then document is valid

    Examples:
    | xml_file               | process    | generated_by | source_id       |
    | applied-processing.xml | creation   | producer.py  | lorem_ipsum.txt |
    | applied-processing.xml | validation | producer.py  |                 |
