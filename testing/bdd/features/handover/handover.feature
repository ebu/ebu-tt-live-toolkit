Feature: Handover algorithm
# when a document is received with a higher value ebuttp:authorsGroupControlToken than that most recently received in the
# currently selected sequence the Handover Manager shall switch to that document's sequence, i.e. it shall emit 
# a document in its output sequence corresponding to the received document with the new control token without delay.

    Examples:
    | xml_file               |  
    | handover_algorithm.xml |  
    

  # SPEC-CONFORMANCE: R23, R25, 120
  Scenario: Switch to sequence with higher value token
    Given an xml file <xml_file>
    And a handover node
    When it has sequence identifier <seq_id_1>
    And it has authorsGroupIdentifier <group_1>
    And it has authorsGroupControlToken <token_1>
    And the document is generated
    And the document is processed 
    And another document arrives 
    And it has sequence identifier <seq_id_2>
    And it has authorsGroupIdentifier <group_2>
    And it has authorsGroupControlToken <token_2>
    And the document is generated
    And the document is processed
    Then the emitted document has <authorsGroupSelectedSequenceIdentifier> 

    Examples:
    | seq_id_1   | group_1 | token_1   | seq_id_2   | group_2 | token_2   | authorsGroupSelectedSequenceIdentifier |  
    | sequence_a | 1       | 12345     | sequence_b | 1       | 12346     | sequence_b                             |  
    | sequence_a | a       | 999999999 | sequence_b | a       | 999999998 | sequence_a                             |  
    | sequence_a | a       | 3         | sequence_a | a       | 3         | sequence_a                             |  


  Scenario: Document with lower value token not emitted
    Given an xml file <xml_file>
    And a handover node
    When it has sequence identifier <seq_id_1>
    And it has authorsGroupControlToken <token_1>
    And the document is generated
    And the document is processed 
    And another document arrives 
    And it has sequence identifier <seq_id_2>
    And it has authorsGroupControlToken <token_2>
    And the document is generated
    And the document is processed
    Then no document is emitted 

    Examples:
    | seq_id_1   | token_1   | seq_id_2   | token_2   |  
    | sequence_a | 2         | sequence_b | 1         |  
    | sequence_a | 999999999 | sequence_b | 999999998 |  



  # SPEC-CONFORMANCE: R24, R125
  # Within a single sequence, all documents that contain  ebuttp:authorsGroupIdentifier shall have the same ebuttp:authorsGroupIdentifier
  Scenario: Different group identifiers in a sequence 
    Given a test sequence
    And an xml file <xml_file>
    When it has sequenceIdentifier 1
    And it has <authorsGroupIdentifier_1>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceIdentifier 1
    And it has <authorsGroupIdentifier_2>
    Then adding doc2 to the sequence results in an error

    Examples:
    | authorsGroupIdentifier_1 | authorsGroupIdentifier_2 |  
    | 1                        | 0                        |  
    | 0                        | 1                        |  
    |                          | 1                        |  
    # ^^^ Assuming NULL means authorsGroupIdentifier is present but empty (if the attribute doesn't exist the document is valid!)


  # SPEC-CONFORMANCE: R121
  # The Handover Manager shall not emit any documents derived from documents that do not contain both the parameters 
  # ebuttp:authorsGroupIdentifier and ebuttp:authorsGroupControlToken.
  Scenario: Documents with missing group identifier and token
    Given an xml file <xml_file>
    And a handover node
    When it does not have attribute authorsGroupControlToken 
    And it does not have attribute authorsGroupIdentifier 
    Then the document is not added to sequence

  Scenario: Documents with missing group identifier
    Given an xml file <xml_file>
    And a handover node
    When it does not have attribute authorsGroupIdentifier 
    Then the document is not added to sequence

  Scenario: Documents with missing token
    Given an xml file <xml_file>
    And a handover node
    When it does not have attribute authorsGroupControlToken 
    Then the document is not added to sequence

  # SPEC-CONFORMANCE: R125
  Scenario: Invalid group identifier
    Given an xml file <xml_file>
    When it has authorsGroupIdentifier <group_1>
    Then adding the document to the sequence results in an error

    Examples:
    | group_1 |  
    |         |  
    # ^^^ HERE WE MEAN AN EMPTY STRING!
