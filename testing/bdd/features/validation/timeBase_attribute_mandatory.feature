# Note: contains examples of SMPTE time base. SMPTE was removed from the specification in version 1.0. -->


@validation @xsd
Feature: ttp:timeBase attribute is mandatory
  Every document shall declare ttp:timeBase

  # SPEC-CONFORMANCE: R32
  Scenario Outline: Invalid ttp:timeBase
    Given an xml file "timeBase_attribute_mandatory.xml"
    When it has ttp:timeBase attribute <time_base>
    Then document is invalid

    Examples:
    | time_base      |
    |                |
    | *?Empty?*      |
    | hello          |
    | wrong timebase |


  # SPEC-CONFORMANCE: R32
  Scenario Outline: Valid ttp:timeBase
    Given an xml file "timeBase_attribute_mandatory.xml"
    When it has ttp:timeBase attribute <time_base>
    Then document is valid

    Examples:
    | time_base |
    | clock     |
    | media     |
    | smpte     |
