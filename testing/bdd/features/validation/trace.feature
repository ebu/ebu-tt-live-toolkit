@validation @syntax @metadata
Feature: Trace element constrainst
  Attributes `action` and `generatedBy` are mandatory.

  # SPEC-CONFORMANCE : R31 R42 R43
  Scenario: Invalid trace attributes
    Given an xml file <xml_file>
    When trace element has action attribute <action>
    And trace element has generatedBy attribute <generated_by>
    And trace element has sourceId attribute <source_id>
    Then document is invalid

    Examples:
    | xml_file  | action   | generated_by | source_id       |
    | trace.xml |          | producer.py  |                 |
    | trace.xml | creation |              |                 |
    | trace.xml |          |              | lorem_ipsum.txt |


Scenario: Valid trace attributes
    Given an xml file <xml_file>
    When trace element has action attribute <action>
    And trace element has generatedBy attribute <generated_by>
    And trace element has sourceId attribute <source_id>
    Then document is valid

    Examples:
    | xml_file  | action     | generated_by | source_id       |
    | trace.xml | creation   | producer.py  | lorem_ipsum.txt |
    | trace.xml | validation | producer.py  |                 |
