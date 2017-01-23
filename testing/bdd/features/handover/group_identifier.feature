Feature: authorsGroupIdentifier consistent within a sequence 

  Examples:
  | xml_file     |  
  | handover.xml |  

  
  # SPEC-CONFROMANCE.md #24
  # All documents within a sequence that contain the element ebuttp:authorsGroupIdentifier shall have the same ebuttp:authorsGroupIdentifier.
  Scenario: Invalid authorsGroupIdentifier
    Given a test sequence
    And an xml file <xml_file>
    And it has sequenceNumber 1
    And it has <ebuttp:authorsGroupIdentifier1>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceNumber 2
    And it has <ebuttp:authorsGroupIdentifier2>
    When doc2 is added to the sequence
    Then adding doc2 to the sequence results in an error

    Examples:
    | ebuttp:authorsGroupIdentifier1 | ebuttp:authorsGroupIdentifier2 |  
    | 0                              | 1                              |  
    # ebuttp:authorsGroupIdentifier="" 
    |                                | 1                              |  
  

  Scenario: Valid authorsGroupIdentifier
    Given a test sequence
    And an xml file <xml_file>
    And it has sequenceNumber 1
    And it has <ebuttp:authorsGroupIdentifier1>
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceNumber 2
    And it has <ebuttp:authorsGroupIdentifier2>
    When doc2 is added to the sequence
    Then adding doc2 to the sequence does not results in any error

    Examples:
    | ebuttp:authorsGroupIdentifier1 | ebuttp:authorsGroupIdentifier2 |  
    | 0                              | 1                              |  
    # ebuttp:authorsGroupIdentifier=""   
    |                                |                                |  



  Scenario: No authorsGroupIdentifier
    Given a test sequence
    And an xml file <xml_file>
    And it has sequenceNumber 1
    And it does not have element ebuttp:authorsGroupIdentifier
    And doc1 is added to the sequence
    And we create a new document
    And it has sequenceNumber 2
    And it has element ebuttp:authorsGroupIdentifier1
    When doc2 is added to the sequence
    Then adding doc2 to the sequence does not results in any error

