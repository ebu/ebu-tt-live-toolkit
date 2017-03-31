Feature: Handover algorithm
# when a document is received with a higher value ebuttp:authorsGroupControlToken than that most recently received in the
# currently selected sequence the Handover Manager shall switch to that document's sequence, i.e. it shall emit 
# a document in its output sequence corresponding to the received document with the new control token without delay.

    Examples:
    | xml_file            |   
    | handover_algorithm.xml |   
    

  # SPEC-CONFORMANCE: R23, R25, 120
  Scenario: Switch to sequence with higher value token
    Given an xml file <xml_file>
    And a handover node
    When it has sequence identifier <seq_id_1>
    And it has authorsGroupControlToken <token_1>
    And the document is generated
    And the document is processed 
    # ^^^ ASSUMING THIS STEP COVERS CACHED TOKENS, IE THE SECOND DOCUMENTS DOESN'T HAVE TO FOLLOW IMMEDIATELY 
    And another document arrives 
    And it has sequence identifier <seq_id_2>
    And it has authorsGroupControlToken <token_2>
    And the document is generated
    And the document is processed
    Then the emitted document has <authorsGroupSelectedSequenceIdentifier> 

    Examples:
    | seq_id_1   | token_1         | seq_id_2   | token_2         | authorsGroupSelectedSequenceIdentifier |  
    | sequence_a | 12345           | sequence_b | 12346           | sequence_b                             |  
    | sequence_a | 1               | sequence_b | 0               | sequence_a                             |  
    | sequence_a | 0               | sequence_b |                 | sequence_a                             |  
    | sequence_a | 999999999999999 | sequence_b | 999999999999998 | sequence_a                             |  


  # SPEC-CONFORMANCE: R24
  # Within a single sequence, all documents that contain the element ebuttp:authorsGroupIdentifier shall have the same ebuttp:authorsGroupIdentifier
  Scenario: Different group identifiers in a sequence 
    Given a test sequence
    And an xml file <xml_file>
    When it has sequenceNumber 1
    And it has <authorsGroupIdentifier_1>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceNumber 1
    And it has <authorsGroupIdentifier_2>
    Then adding doc2 to the sequence results in an error

    Examples:
    | authorsGroupIdentifier_1 | authorsGroupIdentifier_1 |  
    | 1                        | 0                        |  
    | 0                        | 1                        |  
    |                          | 1                        |  
    # ^^^ Assuming NULL means authordGroupIdentifier is present but empty (if the element doesn't exist the document is valid!)

  Scenario: Missing group identifiers in a sequence 
    Given a test sequence
    And an xml file <xml_file>
    When it has sequenceNumber 1
    And it has <authorsGroupIdentifier_1>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceNumber 1
    And it does not have element authorsGroupIdentifier
    Then doc2 is added to the sequence

    Examples:
    | authorsGroupIdentifier_1 | 
    | 1                        | 


  # SPEC-CONFORMANCE: R121
  # The Handover Manager shall not emit any documents derived from documents that do not contain both the parameters 
  # ebuttp:authorsGroupIdentifier and ebuttp:authorsGroupControlToken.
  Scenario: Documents with missing group identifier and token
    Given an xml file <xml_file>
    And a handover node
    When it does not have element authorsGroupControlToken 
    And it does not have element authorsGroupIdentifier 
    Then the document is not added to sequence





