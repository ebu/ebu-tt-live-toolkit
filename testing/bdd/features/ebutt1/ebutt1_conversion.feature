Feature: Converting EBU-TT Part 1 files
  Examples:
    | xml_file            |
    | ebutt1_template.xml |

@skip
# skip until documentIdentifier in head metadata is supported
  Scenario: Pass conversion check with documentIdentifier in head metadata
    Given an xml file <xml_file>
    When the document head metadata contains a documentIdentifier element
    And the document contains a "styling" element
    And the document contains a "style" element
    And the document contains a "layout" element
    And the document contains a "region" element
    And the XML is parsed as a valid EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the sequenceIdentifier is "headDocId"

  Scenario: Pass conversion check with documentIdentifier in document metadata and converter set to use documentIdentifier as a sequenceIdentifier
    Given an xml file <xml_file>
    When the documentMetadata contains a documentIdentifier element
    And the document contains a "styling" element
    And the document contains a "style" element
    And the document contains a "layout" element
    And the document contains a "region" element
    And the XML is parsed as a valid EBU-TT-1 document
    And the EBU-TT-1 converter is set to use the documentIdentifier as a sequenceIdentifier
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the sequenceIdentifier is "docMetaDocId"


  Scenario: Pass conversion check with documentIdentifier in document metadata and converter set not to use documentIdentifier as a sequenceIdentifier
    Given an xml file <xml_file>
    When the documentMetadata contains a documentIdentifier element
    And the document contains a "styling" element
    And the document contains a "style" element
    And the document contains a "layout" element
    And the document contains a "region" element
    And the XML is parsed as a valid EBU-TT-1 document
    And the EBU-TT-1 converter is set not to use the documentIdentifier as a sequenceIdentifier
    And the EBU-TT-1 converter sequenceIdentifier is "BDDSEQID"
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the sequenceIdentifier is "BDDSEQID"

  Scenario: Pass conversion check with no documentIdentifier
    Given an xml file <xml_file>
    When the document contains a "styling" element
    And the document contains a "style" element
    And the document contains a "layout" element
    And the document contains a "region" element
    And the XML is parsed as a valid EBU-TT-1 document
    And the EBU-TT-1 document is converted to EBU-TT-3
    Then the EBU-TT-3 document is valid
    And the sequenceIdentifier is "TestConverter"
