@handover @node @active
# When present in a document, the ebuttp:authorsGroupControlToken is a number that the
# Handover Manager uses to identify which sequence to select: when a document is received with a
# higher value ebuttp:authorsGroupControlToken than that most recently received in the
# currently selected sequence the Handover Manager shall switch to that document's sequence, i.e. it
# shall emit a document in its output sequence corresponding to the received document with the new
# control token without delay.
# Note: The above definition permits the control token value to be lowered after taking control,
# either by setting the control token value to an explicit lower number or by omitting it in
# subsequent documents and relying on the initial value of "0".

Feature: Handover algorithm

  Examples:
  | xml_file     | sequence_identifier | authors_group_identifier |
  | handover.xml | handoverOutputSeq   | handoverTest01           |


  # SPEC-CONFROMANCE.md R23, R24, R25, R120, R121, R122, R123, R125, R126
  # When a document is received with a higher value ebuttp:authorsGroupControlToken than that most recently received
  # in the currently selected sequence, the Handover Manager shall switch to that document's sequence without delay.
  Scenario: Switch to higher value token and ignore lower value token
    Given a handover node with <authors_group_identifier> and <sequence_identifier>
    And an xml file <xml_file>
    When it has sequence id <sequence_identifier1> and sequence num <sequence_number1>
    And it has authors group identifier <authors_group_identifier>
    And it has authors group control token <authors_group_control_token1>
    And the document is generated
    And handover node processes document
    And new document is created
    And new document has sequence id <sequence_identifier2> and sequence num <sequence_number2>
    And new document has authors group identifier <authors_group_identifier>
    And new document has authors group control token <authors_group_control_token2>
    And the document is generated
    And handover node processes document
    Then handover node emits <emitted_documents> documents
    And the emitted documents have <authors_group_selected_sequence_identifiers>
    And the emitted documents belong to <sequence_identifier> and use consecutive sequence numbering from 1
    And the emitted documents have <authors_group_identifier> and they specify a token

    Examples:
    | sequence_identifier1 | sequence_number1 | authors_group_control_token1 | sequence_identifier2 | sequence_number2 | authors_group_control_token2 | emitted_documents | authors_group_selected_sequence_identifiers |
    | seq1                 | 1                | 1                            | seq2                 | 1                | 2                            | 2                 | seq1,seq2                                   |
    | seq1                 | 1                | 2                            | seq2                 | 1                | 3                            | 2                 | seq1,seq2                                   |
    | seq1                 | 1                |                              | seq2                 | 1                | 1                            | 1                 | seq2                                        |
    # token updated if in the same sequence
    | seq1                 | 1                | 2                            | seq1                 | 2                | 1                            | 2                 | seq1,seq1                                   |
    | seq1                 | 1                | 1                            | seq1                 | 2                | 1                            | 2                 | seq1,seq1                                   |
    | seq1                 | 1                | 1                            | seq1                 | 2                | 2                            | 2                 | seq1,seq1                                   |
    | seq1                 | 1                | 2                            | seq2                 | 1                | 1                            | 1                 | seq1                                        |
    | seq1                 | 1                | 2                            | seq2                 | 1                | 2                            | 1                 | seq1                                        |
    # fails to emit any documents because second doc has same sequence_number as first one, and is discarded.
    | seq1                 | 1                |                              | seq1                 | 1                | 2                            | 0                 |                                             |
