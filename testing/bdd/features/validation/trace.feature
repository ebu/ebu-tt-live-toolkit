@validation @syntax @metadata
Feature: Trace element constrainst
  Attributes `action` and `generatedBy` are mandatory.


  Scenario: Invalid trace attributes
    Given an xml file <xml_file>
    When trace element has action attribute <action>
    And trace element has generatedBy attribute <generated_by>
    Then document is invalid

    Examples:
    | xml_file  | action   | generated_by |
    | trace.xml |          | producer.py  |
    | trace.xml | creation |              |
    | trace.xml |          |              |


Scenario: Valid trace attributes
    Given an xml file <xml_file>
    When trace element has action attribute <action>
    And trace element has generatedBy attribute <generated_by>
    Then document is valid

    Examples:
    | xml_file  | action     | generated_by |
    | trace.xml | creation   | producer.py  |
    | trace.xml | validation | producer.py  |
