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

  
  # SPEC-CONFROMANCE.md R23, R25
  # When a document is received with a higher value ebuttp:authorsGroupControlToken than that most recently received 
  # in the currently selected sequence, the Handover Manager shall switch to that document's sequence without delay.
  Scenario: Switch to higher value token
    Given a handover node with <authors_group_identifier> and <sequence_identifier>
    And an xml file <xml_file> 
    When it has <sequence_identifier1> and <sequence_number1>
    And it has <authors_group_identifier>
    And it has <authors_group_control_token1>
    And the document is generated
    And handover node processes document
    And new document is created
    And it has <sequence_identifier2> and <sequence_number2>
    And it has <authors_group_identifier>
    And it has <authors_group_control_token2>
    And the document is generated
    And handover node processes document
    Then handover node emits <emitted_documents> documents

    Examples:
    | sequence_identifier1 | sequence_number1 | authors_group_control_token1 | sequence_identifier2 | sequence_number2 | authors_group_control_token2 | emitted_documents |
    | seq1                 | 1                | 1                            | seq2                 | 1                | 2                            | 2                 |
    | seq1                 | 1                | 2                            | seq2                 | 1                | 3                            | 2                 |
    | seq1                 | 1                |                              | seq2                 | 1                | 1                            | 1                 |
    # token updated if in the same sequence
    | seq1                 | 1                | 1                            | seq1                 | 2                | 0                            | 2                 |


@skip
 Scenario: Ignore lower value token
    Given a test sequence
    And a handover node with <authors_group_identifier> and <sequence_identifier>
    And an xml file <xml_file> 
    And it has <sequenceIdentifier1>
    And it has <authorsGroupControlToken1>
    And doc1 is added to the sequence
    When a new document arrives
    And it has <sequenceIdentifier2>
    And it has <authorsGroupControlToken2>
    Then doc2 is not added to the sequence 

    Examples:
    | sequenceIdentifier1 | authorsGroupControlToken1 | sequenceIdentifier2 | authorsGroupControlToken2 |  
    | seq1                | 1                         | seq2                | 0                         |  
    | seq1                | 0                         | seq1                | 0                         |  
