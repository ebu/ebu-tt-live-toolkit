@node @passive
Feature: Passive nodes shall not modify documents in any way

  # SPEC-CONFORMANCE: R12
  Scenario: Distributing node does not modify documents
    Given an xml file <xml_file>
    And a distributing node
    When it processes the document
    Then the emitted document is identical to the received one

    Examples:
      | xml_file                    |
      | complete_document_clock.xml |
      | complete_document_media.xml |

  # SPEC-CONFORMANCE: R118 (see note below) R119
  # Note: R118 is not fully implemented because the libraries we use do not fully support XQuery functions
  Scenario: BufferDelay node does not modify documents
    Given an xml file <xml_file>
    And a buffer delay node
    When it delays the document
    Then the delayed document is identical to the received one

    Examples:
      | xml_file                    |
      | complete_document_clock.xml |
      | complete_document_media.xml |

