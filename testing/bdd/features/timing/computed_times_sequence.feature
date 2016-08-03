@timing @resolution
Feature: Resolved times computation in sequence

  Examples:
  | xml_file           | sequence_identifier | time_base | doc1_avail_time | doc1_begin  | doc1_end   | doc1_dur | doc2_avail_time | doc2_begin | doc2_end | doc2_dur  |
  | resolved_times.xml | testSequence1       | clock     | 00:00:00.0      | 00:00:10.0  | 00:00:20.0 |          | 00:00:10.0      | 00:00:30.0 |          | 10s       |


  @skip
  # SPEC-CONFORMANCE: R16 R17
  Scenario: Resolved times in sequence
    Given a sequence <sequence_identifier> with timeBase <time_base>
    And an xml file <xml_file>
    When it has predefined sequenceNumber 1
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has doc1 body begin time <doc1_begin>
    And it has doc1 body end time <doc1_end>
    And it has doc1 body duration <doc1_dur>
    And doc1 is added to the sequence with availability time <doc1_avail_time>
    And we create a new document
    And it has predefined sequenceNumber 2
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has doc2 body begin time <doc2_begin>
    And it has doc2 body end time <doc2_end>
    And it has doc2 body duration <doc2_dur>
    And doc2 is added to the sequence with availability time <doc2_avail_time>
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has predefined sequenceNumber 3
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    Then doc1 has computed begin time <c_begin_doc1>
    And doc1 has computed end time <c_end_doc1>
    And doc2 has computed begin time <c_begin_doc2>
    And doc2 has computed end time <c_end_doc2>
    And doc3 has computed begin time <c_begin_doc3>
    And doc3 has computed end time <c_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin  | doc3_end     | doc3_dur | c_begin_doc1 | c_end_doc1 | c_begin_doc2 | c_end_doc2 | c_begin_doc3 | c_end_doc3 |
    | 00:00:20.0      | 00:00:50.0  | 00:01:00.00  |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:40.0 | 00:00:50.0   | 00:01:00.0 |
    | 00:00:20.0      | 00:00:35.0  | 00:01:00.00  |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:35.0 | 00:00:35.0   | 00:01:00.0 |
