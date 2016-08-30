@node @passive
Feature: Passive nodes shall not modify documents in any way

  # SPEC-CONFORMANCE: R12
  Scenario: Distributing node does not modify documents
    Given an xml file <xml_file>
    And a distributing node
    When it processes the document
    Then the emitted document is identical to the received one

    Examples:
    | xml_file              |
    | complete_document.xml |
