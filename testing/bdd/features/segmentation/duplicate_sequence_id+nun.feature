

Feature: Discard document with already seen pair of sequence identifier and sequence number 

    Examples:
    | xml_file            |   
    | sequence_id_num.xml |   
    

  # SPEC-CONFORMANCE: R107
  Scenario: Discard document
    Given an xml file <xml_file>
    And a processing node
    When it has sequence identifier <seq_id_1>
    And it has sequence number <seq_n_1>
    And the document is generated
    And the document is processed
    And another document arrives
    And it has sequence identifier <seq_id_2>
    And it has sequence number <seq_n_2>
    And the document is generated
    Then the document is not processed

    Examples:
    | seq_id_1 | seq_n_1 | seq_id_2 | seq_n_2 |  
    | n        | 1       | n        | 1       |  
    | 1        | 1       | 1        | 1       |  


  Scenario: Do not discard document
    Given an xml file <xml_file>
    And a processing node
    When it has sequence identifier <seq_id_1>
    And it has sequence number <seq_n_1>
    And the document is generated
    And the document is processed
    And another document arrives
    And it has sequence identifier <seq_id_2>
    And it has sequence number <seq_n_2>
    And the document is generated
    Then the document is processed

    Examples:
    | seq_id_1 | seq_n_1 | seq_id_2 | seq_n_2 |  
    | n        | 1       | n        | 2       |
    | 0        | 1       | 1        | 1       |  


  # SPEC-CONFORMANCE: R108
  @skip
  Scenario: Availability time unchanged when discarding
    Given an xml file <xml_file>
    And a processing node
    And it has sequence identifier <seq_id_1>
    And it has sequence number <seq_n_1>
    And the document is processed
    And the document has availability time <avail_time_1>    
    When a document arrives 
    And it has sequence identifier <seq_id_2> 
    And it has sequence number <seq_n_2> 
    Then the first document has availability time <avail_time_2>

    Examples:
    | seq_id_1 | seq_n_1 | avail_time_1 | seq_id_2 | seq_n_2 | avail_time_2 |  
    | n        | 1       | 00:00:00.000 | n        | 1       | 00:00:00.000 |  
    | n        | 0       | 00:00:01.000 | n        | 0       | 00:00:01     |  
  