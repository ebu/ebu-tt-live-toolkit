@validation @xsd
Feature: xml:lang attribute is mandatory on tt element

  # SPEC-CONFORMANCE: R77
  Scenario: Invalid xml:lang attribute
    Given an xml file <xml_file>
    When it has xml:lang attribute <lang>
    Then document is invalid

    Examples:
    | xml_file               | lang  |
    | xml_lang_attribute.xml |       |


  # SPEC-CONFORMANCE: R77
  Scenario: Valid xml:lang attribute
    Given an xml file <xml_file>
    When it has xml:lang attribute <lang>
    Then document is valid

    Examples:
    | xml_file               | lang      |
    | xml_lang_attribute.xml | *?Empty?* |
    | xml_lang_attribute.xml | en-GB     |
