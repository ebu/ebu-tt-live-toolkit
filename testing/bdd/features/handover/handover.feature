Feature: Handover algorithm
# when a document is received with a higher value ebuttp:authorsGroupControlToken than that most recently received in the
# currently selected sequence the Handover Manager shall switch to that document's sequence, i.e. it shall emit 
# a document in its output sequence corresponding to the received document with the new control token without delay.

    Examples:
    | xml_file     | sequence_identifier | authors_group_identifier |
    | handover.xml | handoverOutputSeq   | handoverTest01           |


  # SPEC-CONFORMANCE: R24, R122
  # Within a single sequence, all documents that contain  ebuttp:authorsGroupIdentifier shall have the same ebuttp:authorsGroupIdentifier
  # The handover node should throw an error when this happens
  Scenario: Different group identifiers in a sequence 
    Given a handover node with <authors_group_identifier> and <sequence_identifier>
    And an xml file <xml_file>
    When it has <sequence_identifier1> and <sequence_number1>
    And it has <authors_group_identifier1>
    And it has <authors_group_control_token1>
    And the document is generated
    And handover node processes document
    And new document is created
    And it has <sequence_identifier2> and <sequence_number2>
    And it has <authors_group_identifier2>
    And it has <authors_group_control_token2>
    And the document is generated
    Then handover node errors when processing document

    Examples:
    | sequence_identifier1 | sequence_number1 | authors_group_identifier1 | authors_group_control_token1 | sequence_identifier2 | sequence_number2 | authors_group_identifier2 | authors_group_control_token2 |
    | seq1                 | 1                | foo                       | 1                            | seq1                 | 2                | bar                       | 2                            |


  # SPEC-CONFORMANCE: R121
  # The Handover Manager shall not emit any documents derived from documents that do not contain both the parameters 
  # ebuttp:authorsGroupIdentifier and ebuttp:authorsGroupControlToken.
  Scenario: Documents with missing group identifier and token
    Given a handover node with <authors_group_identifier> and <sequence_identifier>
    And an xml file <xml_file>
    When it has <sequence_identifier1> and <sequence_number1>
    And it has <authors_group_identifier1>
    And it has <authors_group_control_token1>
    And the document is generated
    And handover node processes document
    Then handover node emits <emitted_documents> documents

    Examples:
    | sequence_identifier1 | sequence_number1 | authors_group_identifier1 | authors_group_control_token1 | emitted_documents |
    | seq1                 | 1                |                           | 10                           | 0                 |
    | seq1                 | 1                | foo                       |                              | 0                 |
    | seq1                 | 1                |                           |                              | 0                 |


  # SPEC-CONFORMANCE: R122
  Scenario: Invalid group identifier
    Given a handover node with <authors_group_identifier> and <sequence_identifier>  # This is line is not needed by the test but otherwise the BDD framework complains of mismatching variables
    And an xml file <xml_file>
    When it has <sequence_identifier1> and <sequence_number1>
    And it has <authors_group_identifier1>
    Then document is invalid

    Examples:
    | sequence_identifier1 | sequence_number1 | authors_group_identifier1 |
    | seq1                 | 1                | *?Empty?*                 |


