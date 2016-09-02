@timing @resolution @sequence
Feature: Splicing documents for sequence 

  # SPEC-CONFORMANCE: R16 R17
  Scenario: Exctract elements for new timeline, 2 documents 
    Given a sequence <sequence_identifier> with timeBase <time_base>
    And an xml file <xml_file>
    And it has doc1 with sequenceNumber <sn_1>
    And doc1 has availability time <avail_1>
    And doc1 has element1 with id <id_1> 
    And element1 has begin time of <begin_1> 
    And element1 has end time of <end_1> 
    And element1 has dur of <dur_1> 
    When doc2 arrives with with sequenceNumber <sn_2>
    And doc2 has availability time <avail_2>
    And doc2 has element2 with id <id_2> 
    And element2 has begin time of <begin_2> 
    And element2 has end time of <end_2> 
    And element2 has dur of <dur_2>
    Then we create a new document doc3 with sequenceNumber <sn_3>
    And doc3 has availability time <avail_3>
    And doc3 has element3 with id <id_3> 
    And element3 has begin time of <begin_3> 
    And element2 has end time of <end_3> 
    And element2 has dur of <dur_3>

    Examples:
    | sn_1 | id_1 | begin_1  | end_1    | sn_2 | id_2 | begin_2  | end_2    | avail_3  | sn_3 | id_3    | begin_3  | end_3    |  
    | 1    | id1  | 00:00:00 | 00:00:20 | 2    | id1  | 00:00:10 | 00:00:30 | 00:00:20 | 3    | SN3_id1 | 00:00:20 | 00:00:30 |  
    | 1    | id1  | 00:00:30 | 00:00:60 | 2    | id2  | 00:40:00 | 00:01:00 | 00:00:50 | 3    | SN3_id2 | 00:50:00 | 00:01:00 |  

