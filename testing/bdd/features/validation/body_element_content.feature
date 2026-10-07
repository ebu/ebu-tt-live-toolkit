@validation @syntax
Feature: Body Element Content testing
  The body element is restricted in terms of allowed child elements

  Scenario Outline: Invalid body element content
    Given an xml file "body_element_content.xml"
    When its body has a <child_element>
    Then document is invalid

    Examples:
    | child_element|
    | span         |
    | p            |
    | br           |
