

Feature: Discard document with already seen pair of sequence identifier and sequence number 

    Examples:
    | xml_file            |   
    | sequence_id_num.xml |   
    

  # SPEC-CONFORMANCE: R107
  Scenario: Discard document
    Given an xml file <xml_file>
    And it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    When a previous document exists with sequence identifier <prev_seq_id> and sequence number <prev_seq_n>
    Then the document is not added to the sequence

    Examples:
    | seq_id | seq_n | prev_seq_id | prev_seq_n |  
    | n      | 1     | n           | 1          |  
    # Leading zeros and + not permitted for xs:positiveInteger so there's not much else we can test here.

  # SPEC-CONFORMANCE: R108
  Scenario: Availability time unchanged when discarding
    Given an xml file <xml_file>
    And it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    When a previous document exists with sequence identifier <prev_seq_id> and sequence number <prev_seq_n> 
    And the previous document is available between <prev_begin> and <prev_end>
    Then the previous document is available between <post_begin> and <post_end>

    Examples:
    | seq_id | seq_n | prev_seq_id | prev_seq_n | prev_begin   | prev_end     | post_begin   | post_end     |  
    | n      | 1     | n           | 1          | 00:00:00.000 | 00:00:00.001 | 00:00:00.000 | 00:00:00.001 |  

  # NOT A CONFORMANCE REQUIREMENT, CAN BE POSTPONED  
  Scenario: Issue warning for non-identical documents
    Given an xml file <xml_file>
    And it has sequence identifier <seq_id>
    And it has sequence number <seq_n>
    And it has hashed value of <MD5>
    When a document exists with sequence identifier <prev_seq_id> and sequence number <prev_seq_n>
    And the previous document has hashed value of <prev_MD5>
    Then the document is not added to the sequence
    And a warning is issued

    Examples:
    | seq_id | seq_n | MD5                              | prev_seq_id | prev_seq_n | prev_MD5                         |  
    | n      | 1     | 2db4f88c4f2b8ad2b15659f40253b90b | n           | 1          | 2db4f88c4f2b8ad2b15659f40253b900 |  