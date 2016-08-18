@validation @xsd
Feature: ttp:timeBase attribute is mandatory
  Every document shall declare ttp:timeBase

  # SPEC-CONFORMANCE: R32
  Scenario: Invalid ttp:timeBase
    Given an xml file <xml_file>
    When it has ttp:timeBase attribute <time_base>
    Then document is invalid

    Examples:
    | xml_file                         | time_base      |
    | timeBase_attribute_mandatory.xml |                |
    | timeBase_attribute_mandatory.xml | *?Empty?*      |
    | timeBase_attribute_mandatory.xml | hello          |
    | timeBase_attribute_mandatory.xml | wrong timebase |


  # SPEC-CONFORMANCE: R32
  Scenario: Valid ttp:timeBase
    Given an xml file <xml_file>
    When it has ttp:timeBase attribute <time_base>
    Then document is valid

    Examples:
    | xml_file                         | time_base |
    | timeBase_attribute_mandatory.xml | clock     |
    | timeBase_attribute_mandatory.xml | media     |
    | timeBase_attribute_mandatory.xml | smpte     |
