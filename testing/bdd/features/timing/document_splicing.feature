@timing @resolution @sequence
Feature: Splicing documents for sequence 

  # SPEC-CONFORMANCE: R16 R17
  Scenario: Extract segment from 2 documents   
    Given a sequence <seq_id> with timeBase <time_base>
    And an xml file <xml_file>
    And it has doc1 with sequenceNumber <seq_no_1>
    And doc1 has availability time <avail_1>
    And doc1 has element1 with id <id_1>
    And element1 has begin time of <begin_1> 
    And element1 has end time of <end_1>
    When doc2 arrives with with sequenceNumber <seq_no_2>
    And doc2 has availability time <avail_2>
    And doc2 has element1 with id <id_2>
    And element2 has begin time of <begin_2> 
    And element2 has end time of <end_2> 
    And we extract a new segment from begin time <begin_seg> to end time <end_seg>
    Then the segment has <seq_id_seg>
    And the segment has sequenceNumber <seq_no_seg>
    And the segment has element <id_seg>
    And the elements has begin time <begin_3>
    And the elements has end time <end_3>


    Examples:
    | seq_id | seq_no_1 | avail_1  | id_1 | begin_1  | end_1    | seq_no_2 | avail_2  | id_2 | begin_2  | end_2    | begin_seg | end_seg  | seq_id_seg | seq_no_seg | id_seg  | begin_3  | end_3    |  
    | SEQ1   | 1        | 00:00:00 | foo  | 00:00:00 | 00:00:20 | 2        | 00:00:05 | foo  | 00:00:20 | 00:00:40 | 00:00:20  | 00:00:50 | SEQ1       | 3          | SN3_foo | 00:00:20 | 00:00:40 |  
    | SEQ1   | 1        | 00:00:00 | foo  | 00:00:10 | 00:00:40 | 2        | 00:00:10 | bar  | 00:00:10 | 00:00:40 | 00:00:20  | 00:00:30 | SEQ1       | 3          | SN3_bar | 00:00:20 | 00:00:30 | 
    | SEQ1   | 2        | 00:00:00 | foo  | 00:00:00 | 00:00:30 | 1        | 00:00:00 | bar  | 00:00:00 | 00:00:30 | 00:00:10  | 00:00:20 | SEQ1       | 3          | SN3_foo | 00:00:20 | 00:00:30 | 


    