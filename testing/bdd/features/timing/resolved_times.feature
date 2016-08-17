@timing @resolution @sequence
Feature: Resolved times computation in sequence

  Examples:
  | xml_file                             | sequence_identifier | time_base | doc1_avail_time | doc1_begin  | doc1_end   | doc1_dur | doc2_avail_time | doc2_begin | doc2_end | doc2_dur  |
  | computed_resolved_time_semantics.xml | testSequence1       | clock     | 00:00:01.0      | 00:00:10.0  | 00:00:20.0 |          | 00:00:05.0      | 00:00:30.0 |          | 10s       |

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
    And we create a new document
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has predefined sequenceNumber 3
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    Then doc1 has resolved begin time <r_begin_doc1>
    And doc1 has resolved end time <r_end_doc1>
    And doc2 has resolved begin time <r_begin_doc2>
    And doc2 has resolved end time <r_end_doc2>
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin  | doc3_end    | doc3_dur | r_begin_doc1 | r_end_doc1 | r_begin_doc2 | r_end_doc2 | r_begin_doc3 | r_end_doc3 |
    | 00:00:20.0      | 00:00:50.0  | 00:01:00.0  |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:40.0 | 00:00:50.0   | 00:01:00.0 |
    | 00:00:03.0      | 00:00:50.0  | 00:01:00.0  |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:40.0 | 00:00:50.0   | 00:01:00.0 |
    | 00:00:20.0      | 00:00:35.0  | 00:01:00.0  |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:35.0 | 00:00:35.0   | 00:01:00.0 |


  # SPEC-CONFORMANCE: R16 R17
  Scenario: Resolved times in sequence, document 2 skipped
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
    And we create a new document
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has predefined sequenceNumber 3
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    Then doc2 has resolved_end < resolved_begin and is skipped
    And doc1 has resolved begin time <r_begin_doc1>
    And doc1 has resolved end time <r_end_doc1>
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin  | doc3_end    | doc3_dur | r_begin_doc1 | r_end_doc1 | r_begin_doc3 | r_end_doc3 |
    | 00:00:02.0      | 00:00:25.0  | 00:01:00.0  |          | 00:00:10.0   | 00:00:20.0 | 00:00:25.0   | 00:01:00.0 |
    | 00:00:15.0      | 00:00:16.0  | 00:00:35.0  |          | 00:00:10.0   | 00:00:16.0 | 00:00:16.0   | 00:00:35.0 |


  # SPEC-CONFORMANCE: R16 R17
  Scenario: Resolved times in sequence, document 1 and 2 skipped
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
    And we create a new document
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has predefined sequenceNumber 3
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    Then doc1 and doc2 have resolved_end < resolved_begin and are skipped
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin  | doc3_end     | doc3_dur | r_begin_doc3 | r_end_doc3  |
    | 00:00:08.0      | 00:00:09.23 |              | 1h       | 00:00:09.23  | 01:00:09.23 |
    | 00:00:00.0      | 00:00:09.0  |              | 1h       | 00:00:09.0   | 01:00:09.0  |
    | 00:00:00.0      | 00:00:04.0  |              | 1h       | 00:00:04.0   | 01:00:04.0  |


  # SPEC-CONFORMANCE: R16 R17
  Scenario: Out of order delivery of documents (applicable with some carriage mechanisms)
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
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has predefined sequenceNumber 3
    And it has doc3 body begin time <doc3_begin>
    And it has doc3 body end time <doc3_end>
    And it has doc3 body duration <doc3_dur>
    And doc3 is added to the sequence with availability time <doc3_avail_time>
    And we create a new document
    And it has predefined sequenceNumber 2
    And it has sequenceIdentifier <sequence_identifier>
    And it has timeBase <time_base>
    And it has doc2 body begin time <doc2_begin>
    And it has doc2 body end time <doc2_end>
    And it has doc2 body duration <doc2_dur>
    And doc2 is added to the sequence with availability time <doc2_avail_time>
    Then doc1 has resolved begin time <r_begin_doc1>
    And doc1 has resolved end time <r_end_doc1>
    And doc2 has resolved begin time <r_begin_doc2>
    And doc2 has resolved end time <r_end_doc2>
    And doc3 has resolved begin time <r_begin_doc3>
    And doc3 has resolved end time <r_end_doc3>

    Examples:
    | doc3_avail_time | doc3_begin  | doc3_end    | doc3_dur | r_begin_doc1 | r_end_doc1 | r_begin_doc2 | r_end_doc2 | r_begin_doc3 | r_end_doc3 |
    | 00:00:03.0      | 00:00:50.0  | 00:01:00.0  |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:40.0 | 00:00:50.0   | 00:01:00.0 |
    | 00:00:03.0      | 00:00:38.0  | 00:01:00.0  |          | 00:00:10.0   | 00:00:20.0 | 00:00:30.0   | 00:00:38.0 | 00:00:38.0   | 00:01:00.0 |
