#  When present in a document, the ebuttp:authorsGroupControlToken is a number that the
#  Handover Manager uses to identify which sequence to select: when a document is received with a
#  higher value ebuttp:authorsGroupControlToken than that most recently received in the
#  currently selected sequence the Handover Manager shall switch to that document's sequence, i.e. it
#  shall emit a document in its output sequence corresponding to the received document with the new
#  control token without delay.
#  Note: The above definition permits the control token value to be lowered after taking control,
#  either by setting the control token value to an explicit lower number or by omitting it in
#  subsequent documents and relying on the initial value of "0".

Feature: Handover algorithm  

  Examples:
  | xml_file     |  
  | handover.xml |  

  
  # SPEC-CONFROMANCE.md #23, #25
  # When a document is received with a higher value ebuttp:authorsGroupControlToken than that most recently received 
  # in the currently selected sequence, the Handover Manager shall switch to that document's sequence without delay.
  Scenario: Switch to higher value token
    Given a test sequence
    And an xml file <xml_file> 
    And it has <sequenceIdentifier1>
    And it has <authorsGroupControlToken1>
    And doc1 is added to the sequence
    When a new document arrives
    And it has <sequenceIdentifier2>
    And it has <authorsGroupControlToken2>
    Then doc2 is added to the sequence 

    Examples:
    | sequenceIdentifier1 | authorsGroupControlToken1 | sequenceIdentifier2 | authorsGroupControlToken2 |  
    | seq1                | 1                         | seq2                | 2                         |  
    | seq1                | 0                         | seq2                | 1                         |  
    | seq1                |                           | seq2                | 1                         |  
    # token ignored if in the same sequence
    | seq1                | 1                         | seq1                | 0                         |  


 Scenario: Ignore lower value token
    Given a test sequence
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
