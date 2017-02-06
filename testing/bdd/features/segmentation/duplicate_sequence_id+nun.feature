

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
    And the previous document has availability time <prev_avail>
    Then the previous document has availability time <post_avail>

    Examples:
    | seq_id | seq_n | prev_seq_id | prev_seq_n | prev_avail   | post_avail   |  
    | n      | 1     | n           | 1          | 00:00:00.000 | 00:00:00.000 | 
     

  