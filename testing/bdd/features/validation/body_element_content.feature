@validation @syntax
Feature: Body Element Content testing
  The body element is restricted in terms of allowed child elements

  Scenario: Invalid body element content
    Given an xml file <xml_file>
    When its body has a <child_element>
    Then document is invalid

    Examples:
    | xml_file                 | child_element|
    | body_element_content.xml | span         |
    | body_element_content.xml | p            |
    | body_element_content.xml | br           |
